##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Implements Edb Functions/Edb Procedures Node."""

import copy
import re
from functools import wraps

import pgadmin.browser.server_groups.servers.databases.schemas.packages as packages
from flask import render_template, make_response
from flask_babel import gettext
from pgadmin.browser.collection import CollectionNodeModule
from pgadmin.browser.server_groups.servers.databases.schemas.utils import \
    DataTypeReader
from pgadmin.browser.utils import PGChildNodeView
from pgadmin.utils.ajax import make_json_response, \
    make_response as ajax_response, internal_server_error, gone
from pgadmin.utils.ajax import precondition_required
from pgadmin.utils.driver import get_driver
from pgadmin.utils.preferences import Preferences

from config import PG_DEFAULT_DRIVER


class EdbFuncModule(CollectionNodeModule):
    """
    class EdbFuncModule(CollectionNodeModule):

        This class represents The Functions Module.

    Methods:
    -------
    * __init__(*args, **kwargs)
      - Initialize the Functions Module.

    * get_nodes(gid, sid, did, scid)
      - Generate the Functions collection node.

    * node_inode():
      - Returns Functions node as leaf node.

    * script_load()
      - Load the module script for Functions, when schema node is
        initialized.

    * csssnippets()
      - Returns a snippet of css.
    """

    NODE_TYPE = 'edbfunc'
    COLLECTION_LABEL = gettext("Functions")

    def __init__(self, *args, **kwargs):
        """
        Initialize the Function Module.
        Args:
            *args:
            **kwargs:
        """
        super(EdbFuncModule, self).__init__(*args, **kwargs)

        self.min_ver = 90100
        self.max_ver = None
        self.server_type = ['ppas']

    def get_nodes(self, gid, sid, did, scid, pkgid):
        """
        Generate Functions collection node.
        """
        yield self.generate_browser_collection_node(pkgid)

    @property
    def script_load(self):
        """
        Load the module script for Functions, when the
        package node is initialized.
        """
        return packages.PackageModule.NODE_TYPE

    @property
    def node_inode(self):
        """
        Make the node as leaf node.
        Returns:
            False as this node doesn't have child nodes.
        """
        return False

    def register_preferences(self):
        """
        Register preferences for this module.
        """
        # Add the node informaton for browser, not in respective
        # node preferences
        self.browser_preference = Preferences.module('browser')
        self.pref_show_system_objects = self.browser_preference.preference(
            'show_system_objects'
        )
        self.pref_show_node = self.browser_preference.register(
            'node', 'show_node_' + self.node_type,
            gettext('Package {0}').format(self.label), 'boolean',
            self.SHOW_ON_BROWSER, category_label=gettext('Nodes')
        )


blueprint = EdbFuncModule(__name__)


class EdbFuncView(PGChildNodeView, DataTypeReader):
    """
    class EdbFuncView(PGChildNodeView, DataTypeReader)

    This class inherits PGChildNodeView and DataTypeReader to get the different routes for
    the module.

    The class is responsible to Create, Read, Update and Delete operations for
    the Functions.

    Methods:
    -------
    * validate_request(f):
      - Works as a decorator.
        Validating request on the request of create, update and modified SQL.

    * module_js():
      - Overrides this property to define javascript for Functions node.

    * check_precondition(f):
      - Works as a decorator.
      - Checks database connection status.
      - Attach connection object and template path.

    * list(gid, sid, did, scid, pkgid):
      - List the Functions.

    * nodes(gid, sid, did, scid, pkgid):
      - Returns all the Functions to generate Nodes in the browser.

    * properties(gid, sid, did, scid, pkgid, edbfnid):
      - Returns the Functions properties.

    * sql(gid, sid, did, scid, pkgid, edbfnid):
      - Returns the SQL for the Functions object.

    * dependents(gid, sid, did, scid, ,pkgid, edbfnid):
      - Returns the dependents for the Functions object.

    * dependencies(gid, sid, did, scid, pkgid, edbfnid):
      - Returns the dependencies for the Functions object.

    """

    node_type = blueprint.node_type

    parent_ids = [
        {'type': 'int', 'id': 'gid'},
        {'type': 'int', 'id': 'sid'},
        {'type': 'int', 'id': 'did'},
        {'type': 'int', 'id': 'scid'},
        {'type': 'int', 'id': 'pkgid'}
    ]
    ids = [
        {'type': 'int', 'id': 'edbfnid'}
    ]

    operations = dict({
        'obj': [
            {'get': 'properties'},
            {'get': 'list'}
        ],
        'nodes': [{'get': 'nodes'}, {'get': 'nodes'}],
        'sql': [{'get': 'sql'}],
        'dependency': [{'get': 'dependencies'}],
        'dependent': [{'get': 'dependents'}],
        'module.js': [{}, {}, {'get': 'module_js'}]
    })

    def module_js(self):
        """
        Load JS file (functions.js) for this module.
        """

        return make_response(
            render_template(
                "edbfunc/js/edbfunc.js",
                _=gettext
            ),
            200, {'Content-Type': 'application/x-javascript'}
        )

    def check_precondition(f):
        """
        Works as a decorator.
        Checks the database connection status.
        Attaches the connection object and template path to the class object.
        """

        @wraps(f)
        def wrap(*args, **kwargs):
            self = args[0]
            driver = get_driver(PG_DEFAULT_DRIVER)
            self.manager = driver.connection_manager(kwargs['sid'])

            # Get database connection
            self.conn = self.manager.connection(did=kwargs['did'])

            self.qtIdent = driver.qtIdent
            self.qtLiteral = driver.qtLiteral

            if not self.conn.connected():
                return precondition_required(
                    gettext(
                        "Connection to the server has been lost!"
                    )
                )

            # Set template path for sql scripts depending
            # on the server version.

            self.sql_template_path = "/".join([
                self.node_type,
                self.manager.server_type,
                '#{0}#'
            ]).format(self.manager.version)

            return f(*args, **kwargs)

        return wrap

    @check_precondition
    def list(self, gid, sid, did, scid, pkgid):
        """
        List all the Functions.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
        """

        SQL = render_template("/".join([self.sql_template_path, 'node.sql']),
                              pkgid=pkgid)
        status, res = self.conn.execute_dict(SQL)

        if not status:
            return internal_server_error(errormsg=res)
        return ajax_response(
            response=res['rows'],
            status=200
        )

    @check_precondition
    def nodes(self, gid, sid, did, scid, pkgid, edbfnid=None):
        """
        Returns all the Functions to generate the Nodes.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
        """

        res = []
        SQL = render_template(
            "/".join([self.sql_template_path, 'node.sql']),
            pkgid=pkgid,
            fnid=edbfnid
        )
        status, rset = self.conn.execute_2darray(SQL)

        if not status:
            return internal_server_error(errormsg=rset)

        if edbfnid is not None:
            if len(rset['rows']) == 0:
                return gone(
                    errormsg=_("Could not find the function")
                )
            row = rset['rows'][0]
            return make_json_response(
                data=self.blueprint.generate_browser_node(
                    row['oid'],
                    pkgid,
                    row['name'],
                    icon="icon-" + self.node_type
                ),
                status=200
            )

        for row in rset['rows']:
            res.append(
                self.blueprint.generate_browser_node(
                    row['oid'],
                    pkgid,
                    row['name'],
                    icon="icon-" + self.node_type
                ))

        return make_json_response(
            data=res,
            status=200
        )

    @check_precondition
    def properties(self, gid, sid, did, scid, pkgid, edbfnid=None):
        """
        Returns the Function properties.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
            pkgid: Package Id
            edbfnid: Function Id
        """
        SQL = render_template("/".join([self.sql_template_path,
                                        'properties.sql']),
                              pkgid=pkgid, edbfnid=edbfnid)
        status, res = self.conn.execute_dict(SQL)
        if not status:
            return internal_server_error(errormsg=res)

        if len(res['rows']) == 0:
            return gone(gettext("""
Could not find the function in the database.\n
It may have been removed by another user or moved to another schema.
"""))

        resp_data = res['rows'][0]

        # Get formatted Arguments
        frmtd_params, frmtd_proargs = self._format_arguments_from_db(resp_data)
        resp_data.update(frmtd_params)
        resp_data.update(frmtd_proargs)

        return ajax_response(
            response=resp_data,
            status=200
        )

    def _format_arguments_from_db(self, data):
        """
        Create Argument list of the Function.

        Args:
            data: Function Data

        Returns:
            Function Arguments in the following format.
                [
                {'proargtypes': 'integer', 'proargmodes: 'IN',
                'proargnames': 'column1', 'proargdefaultvals': 1}, {...}
                ]
            Where
                Arguments:
                    proargtypes: Argument Types (Data Type)
                    proargmodes: Argument Modes [IN, OUT, INOUT, VARIADIC]
                    proargnames: Argument Name
                    proargdefaultvals: Default Value of the Argument
        """
        proargtypes = [ptype for ptype in data['proargtypenames'].split(",")] \
            if data['proargtypenames'] else []
        proargmodes = data['proargmodes'] if data['proargmodes'] else []
        proargnames = data['proargnames'] if data['proargnames'] else []
        proargdefaultvals = [ptype for ptype in
                             data['proargdefaultvals'].split(",")] \
            if data['proargdefaultvals'] else []
        proallargtypes = data['proallargtypes'] \
            if data['proallargtypes'] else []

        proargmodenames = {'i': 'IN', 'o': 'OUT', 'b': 'INOUT',
                           'v': 'VARIADIC', 't': 'TABLE'}

        # The proargtypes doesn't give OUT params, so we need to fetch
        # those from database explicitly, below code is written for this
        # purpose.
        #
        # proallargtypes gives all the Function's argument including OUT,
        # but we have not used that column; as the data type of this
        # column (i.e. oid[]) is not supported by oidvectortypes(oidvector)
        # function which we have used to fetch the datatypes
        # of the other parameters.

        proargmodes_fltrd = copy.deepcopy(proargmodes)
        proargnames_fltrd = []
        cnt = 0
        for m in proargmodes:
            if m == 'o':  # Out Mode
                SQL = render_template("/".join([self.sql_template_path,
                                                'get_out_types.sql']),
                                      out_arg_oid=proallargtypes[cnt])
                status, out_arg_type = self.conn.execute_scalar(SQL)
                if not status:
                    return internal_server_error(errormsg=out_arg_type)

                # Insert out parameter datatype
                proargtypes.insert(cnt, out_arg_type)
                proargdefaultvals.insert(cnt, '')
            elif m == 'v':  # Variadic Mode
                proargdefaultvals.insert(cnt, '')
            elif m == 't':  # Table Mode
                proargmodes_fltrd.remove(m)
                proargnames_fltrd.append(proargnames[cnt])

            cnt += 1

        cnt = 0
        # Map param's short form to its actual name. (ex: 'i' to 'IN')
        for m in proargmodes_fltrd:
            proargmodes_fltrd[cnt] = proargmodenames[m]
            cnt += 1

        # Removes Argument Names from the list if that argument is removed
        # from the list
        for i in proargnames_fltrd:
            proargnames.remove(i)

        # Insert null value against the parameters which do not have
        # default values.
        if len(proargmodes_fltrd) > len(proargdefaultvals):
            dif = len(proargmodes_fltrd) - len(proargdefaultvals)
            while (dif > 0):
                proargdefaultvals.insert(0, '')
                dif -= 1

        # Prepare list of Argument list dict to be displayed in the Data Grid.
        params = {"arguments": [
            self._map_arguments_dict(
                i, proargmodes_fltrd[i] if len(proargmodes_fltrd) > i else '',
                proargtypes[i] if len(proargtypes) > i else '',
                proargnames[i] if len(proargnames) > i else '',
                proargdefaultvals[i] if len(proargdefaultvals) > i else ''
            )
            for i in range(len(proargtypes))]}

        # Prepare string formatted Argument to be displayed in the Properties
        # panel.

        proargs = [self._map_arguments_list(
            proargmodes_fltrd[i] if len(proargmodes_fltrd) > i else '',
            proargtypes[i] if len(proargtypes) > i else '',
            proargnames[i] if len(proargnames) > i else '',
            proargdefaultvals[i] if len(proargdefaultvals) > i else ''
        )
                   for i in range(len(proargtypes))]

        proargs = {"proargs": ", ".join(proargs)}

        return params, proargs

    def _map_arguments_dict(self, argid, argmode, argtype, argname, argdefval):
        """
        Returns Dict of formatted Arguments.
        Args:
            argid: Argument Sequence Number
            argmode: Argument Mode
            argname: Argument Name
            argtype: Argument Type
            argdef: Argument Default Value
        """
        # The pg_get_expr(proargdefaults, 'pg_catalog.pg_class'::regclass) SQL
        # statement gives us '-' as a default value for INOUT mode.
        # so, replacing it with empty string.
        if argmode == 'INOUT' and argdefval.strip() == '-':
            argdefval = ''

        return {"argid": argid,
                "argtype": argtype.strip() if argtype is not None else '',
                "argmode": argmode,
                "argname": argname,
                "argdefval": argdefval}

    def _map_arguments_list(self, argmode, argtype, argname, argdef):
        """
        Returns List of formatted Arguments.
        Args:
            argmode: Argument Mode
            argname: Argument Name
            argtype: Argument Type
            argdef: Argument Default Value
        """
        # The pg_get_expr(proargdefaults, 'pg_catalog.pg_class'::regclass) SQL
        # statement gives us '-' as a default value for INOUT mode.
        # so, replacing it with empty string.
        if argmode == 'INOUT' and argdef.strip() == '-':
            argdef = ''

        arg = ''

        if argmode and argmode:
            arg += argmode + " "
        if argname:
            arg += argname + " "
        if argtype:
            arg += argtype + " "
        if argdef:
            arg += " DEFAULT " + argdef

        return arg.strip(" ")

    @check_precondition
    def sql(self, gid, sid, did, scid, pkgid, edbfnid=None):
        """
        Returns the SQL for the Function object.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
            fnid: Function Id
        """
        SQL = render_template("/".join([self.sql_template_path, 'get_body.sql']),
                              scid=scid,
                              pkgid=pkgid)

        status, res = self.conn.execute_dict(SQL)
        if not status:
            return internal_server_error(errormsg=res)

        body = self.get_inner(res['rows'][0]['pkgbodysrc'])

        if body is None:
            body = ''

        SQL = render_template("/".join([self.sql_template_path,
                                        'get_name.sql']),
                              edbfnid=edbfnid)

        status, name = self.conn.execute_scalar(SQL)

        if not status:
            return internal_server_error(errormsg=res)

        sql = u"-- Package {}: {}".format(
            'Function' if self.node_type == 'edbfunc' else 'Procedure',
            name)
        if body != '':
            sql += "\n\n"
            sql += body

        return ajax_response(response=sql)

    @check_precondition
    def dependents(self, gid, sid, did, scid, pkgid, edbfnid):
        """
        This function get the dependents and return ajax response
        for the Function node.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
            doid: Function Id
        """
        dependents_result = self.get_dependents(self.conn, edbfnid)
        return ajax_response(
            response=dependents_result,
            status=200
        )

    @check_precondition
    def dependencies(self, gid, sid, did, scid, pkgid, edbfnid):
        """
        This function get the dependencies and return ajax response
        for the Function node.

        Args:
            gid: Server Group Id
            sid: Server Id
            did: Database Id
            scid: Schema Id
            doid: Function Id
        """
        dependencies_result = self.get_dependencies(self.conn, edbfnid)
        return ajax_response(
            response=dependencies_result,
            status=200
        )

    @staticmethod
    def get_inner(sql):
        if sql is None:
            return None
        start = 0
        start_position = re.search("\s+[is|as]+\s+", sql, flags=re.I)

        if start_position:
            start = start_position.start() + 4

        try:
            end_position = [i for i in re.finditer("end", sql, flags=re.I)][-1]
            end = end_position.start()
        except IndexError:
            return sql[start:].strip("\n")

        return sql[start:end].strip("\n")

EdbFuncView.register_node_view(blueprint)


class EdbProcModule(CollectionNodeModule):
    """
    class EdbProcModule(CollectionNodeModule):

        This class represents The Procedures Module.

    Methods:
    -------
    * __init__(*args, **kwargs)
      - Initialize the Procedures Module.

    * get_nodes(gid, sid, did, scid)
      - Generate the Procedures collection node.

    * node_inode():
      - Returns Procedures node as leaf node.

    * script_load()
      - Load the module script for Procedures, when schema node is
        initialized.

    """

    NODE_TYPE = 'edbproc'
    COLLECTION_LABEL = gettext("Procedures")

    def __init__(self, *args, **kwargs):
        """
        Initialize the Procedure Module.
        Args:
            *args:
            **kwargs:
        """
        super(EdbProcModule, self).__init__(*args, **kwargs)

        self.min_ver = 90100
        self.max_ver = None
        self.server_type = ['ppas']

    def get_nodes(self, gid, sid, did, scid, pkgid):
        """
        Generate Procedures collection node.
        """
        yield self.generate_browser_collection_node(pkgid)

    @property
    def node_inode(self):
        """
        Make the node as leaf node.
        Returns:
            False as this node doesn't have child nodes.
        """
        return False

    @property
    def script_load(self):
        """
        Load the module script for Procedures, when the
        database node is initialized.
        """
        return packages.PackageModule.NODE_TYPE

    def register_preferences(self):
        """
        Register preferences for this module.
        """
        # Add the node informaton for browser, not in respective
        # node preferences
        self.browser_preference = Preferences.module('browser')
        self.pref_show_system_objects = self.browser_preference.preference(
            'show_system_objects'
        )
        self.pref_show_node = self.browser_preference.register(
            'node', 'show_node_' + self.node_type,
            gettext('Package {0}').format(self.label), 'boolean',
            self.SHOW_ON_BROWSER, category_label=gettext('Nodes')
        )

procedure_blueprint = EdbProcModule(__name__)


class EdbProcView(EdbFuncView):
    node_type = procedure_blueprint.node_type

    def module_js(self):
        """
        Load JS file (procedures.js) for this module.
        """

        return make_response(
            render_template(
                "edbproc/js/edbproc.js",
                _=gettext
            ),
            200, {'Content-Type': 'application/x-javascript'}
        )


EdbProcView.register_node_view(procedure_blueprint)
