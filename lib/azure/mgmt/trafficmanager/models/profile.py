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

from .resource import Resource


class Profile(Resource):
    """Class representing a Traffic Manager profile.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Resource Id
    :vartype id: str
    :ivar name: Resource name
    :vartype name: str
    :ivar type: Resource type
    :vartype type: str
    :param location: Resource location
    :type location: str
    :param tags: Resource tags
    :type tags: dict
    :param profile_status: Gets or sets the status of the Traffic Manager
     profile.  Possible values are 'Enabled' and 'Disabled'.
    :type profile_status: str
    :param traffic_routing_method: Gets or sets the traffic routing method of
     the Traffic Manager profile.  Possible values are 'Performance',
     'Weighted', 'Priority' or 'Geographic'.
    :type traffic_routing_method: str
    :param dns_config: Gets or sets the DNS settings of the Traffic Manager
     profile.
    :type dns_config: :class:`DnsConfig
     <azure.mgmt.trafficmanager.models.DnsConfig>`
    :param monitor_config: Gets or sets the endpoint monitoring settings of
     the Traffic Manager profile.
    :type monitor_config: :class:`MonitorConfig
     <azure.mgmt.trafficmanager.models.MonitorConfig>`
    :param endpoints: Gets or sets the list of endpoints in the Traffic
     Manager profile.
    :type endpoints: list of :class:`Endpoint
     <azure.mgmt.trafficmanager.models.Endpoint>`
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'profile_status': {'key': 'properties.profileStatus', 'type': 'str'},
        'traffic_routing_method': {'key': 'properties.trafficRoutingMethod', 'type': 'str'},
        'dns_config': {'key': 'properties.dnsConfig', 'type': 'DnsConfig'},
        'monitor_config': {'key': 'properties.monitorConfig', 'type': 'MonitorConfig'},
        'endpoints': {'key': 'properties.endpoints', 'type': '[Endpoint]'},
    }

    def __init__(self, location=None, tags=None, profile_status=None, traffic_routing_method=None, dns_config=None, monitor_config=None, endpoints=None):
        super(Profile, self).__init__(location=location, tags=tags)
        self.profile_status = profile_status
        self.traffic_routing_method = traffic_routing_method
        self.dns_config = dns_config
        self.monitor_config = monitor_config
        self.endpoints = endpoints