# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .sub_resource import SubResource


class ApplicationGatewayRequestRoutingRule(SubResource):
    """Request routing rule of an application gateway.

    :param id: Resource ID.
    :type id: str
    :param rule_type: Rule type. Possible values are: 'Basic' and
     'PathBasedRouting'. Possible values include: 'Basic', 'PathBasedRouting'
    :type rule_type: str or :class:`ApplicationGatewayRequestRoutingRuleType
     <azure.mgmt.network.v2016_09_01.models.ApplicationGatewayRequestRoutingRuleType>`
    :param backend_address_pool: Backend address pool resource of the
     application gateway.
    :type backend_address_pool: :class:`SubResource
     <azure.mgmt.network.v2016_09_01.models.SubResource>`
    :param backend_http_settings: Frontend port resource of the application
     gateway.
    :type backend_http_settings: :class:`SubResource
     <azure.mgmt.network.v2016_09_01.models.SubResource>`
    :param http_listener: Http listener resource of the application gateway.
    :type http_listener: :class:`SubResource
     <azure.mgmt.network.v2016_09_01.models.SubResource>`
    :param url_path_map: URL path map resource of the application gateway.
    :type url_path_map: :class:`SubResource
     <azure.mgmt.network.v2016_09_01.models.SubResource>`
    :param provisioning_state: Provisioning state of the request routing rule
     resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
    :type provisioning_state: str
    :param name: Name of the resource that is unique within a resource group.
     This name can be used to access the resource.
    :type name: str
    :param etag: A unique read-only string that changes whenever the resource
     is updated.
    :type etag: str
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'rule_type': {'key': 'properties.ruleType', 'type': 'str'},
        'backend_address_pool': {'key': 'properties.backendAddressPool', 'type': 'SubResource'},
        'backend_http_settings': {'key': 'properties.backendHttpSettings', 'type': 'SubResource'},
        'http_listener': {'key': 'properties.httpListener', 'type': 'SubResource'},
        'url_path_map': {'key': 'properties.urlPathMap', 'type': 'SubResource'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
    }

    def __init__(self, id=None, rule_type=None, backend_address_pool=None, backend_http_settings=None, http_listener=None, url_path_map=None, provisioning_state=None, name=None, etag=None):
        super(ApplicationGatewayRequestRoutingRule, self).__init__(id=id)
        self.rule_type = rule_type
        self.backend_address_pool = backend_address_pool
        self.backend_http_settings = backend_http_settings
        self.http_listener = http_listener
        self.url_path_map = url_path_map
        self.provisioning_state = provisioning_state
        self.name = name
        self.etag = etag