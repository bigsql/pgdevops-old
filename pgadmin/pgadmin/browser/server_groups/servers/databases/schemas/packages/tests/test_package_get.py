# #################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
# ##################################################################

import uuid

from regression import test_utils as utils
from regression import parent_node_dict
from pgadmin.utils.route import BaseTestGenerator
from pgadmin.browser.server_groups.servers.tests import utils as server_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from . import utils as package_utils


class PackageGetTestCase(BaseTestGenerator):
    """ This class will fetch new package under test schema. """

    scenarios = [
        # Fetching default URL for package node.
        ('Fetch Package Node URL', dict(
            url='/browser/package/obj/'))
    ]

    def setUp(self):

        schema_info = parent_node_dict["schema"][-1]
        self.schema_id = schema_info["schema_id"]
        self.schema_name = schema_info["schema_name"]
        self.db_name = parent_node_dict["database"][-1]["db_name"]
        self.pkg_name= "pkg_%s" % str(uuid.uuid4())[1:4]
        self.proc_name = "proc_%s" % str(uuid.uuid4())[1:4]
        self.server_id = schema_info["server_id"]
        self.db_id = schema_info["db_id"]
        server_con = server_utils.connect_server(self, self.server_id)

        if server_con:
            if "type" in server_con["data"]:
                if server_con["data"]["type"] == "pg":
                    message = "Packages are not supported by PG."
                    self.skipTest(message)

        self.package_id = package_utils.create_package(self.server,
                                                       self.db_name,
                                                       self.schema_name,
                                                       self.pkg_name,
                                                       self.proc_name)

    def runTest(self):
        """ This function will fetch package under test schema. """

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)

        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      self.schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        response = self.tester.get(self.url
                    + str(utils.SERVER_GROUP) + '/' +
                    str(self.server_id) + '/' + str(self.db_id) + '/' +
                    str(self.schema_id) + '/' + str(self.package_id),
                    content_type='html/json')

        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        """This function disconnect the test database."""

        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
