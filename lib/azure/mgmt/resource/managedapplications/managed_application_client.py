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

from msrest.service_client import ServiceClient
from msrest import Serializer, Deserializer
from msrestazure import AzureConfiguration
from .version import VERSION
from .operations.appliances_operations import AppliancesOperations
from .operations.appliance_definitions_operations import ApplianceDefinitionsOperations
from . import models


class ManagedApplicationClientConfiguration(AzureConfiguration):
    """Configuration for ManagedApplicationClient
    Note that all parameters used to create this instance are saved as instance
    attributes.

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        if credentials is None:
            raise ValueError("Parameter 'credentials' must not be None.")
        if subscription_id is None:
            raise ValueError("Parameter 'subscription_id' must not be None.")
        if not isinstance(subscription_id, str):
            raise TypeError("Parameter 'subscription_id' must be str.")
        if not base_url:
            base_url = 'https://management.azure.com'

        super(ManagedApplicationClientConfiguration, self).__init__(base_url)

        self.add_user_agent('managedapplicationclient/{}'.format(VERSION))
        self.add_user_agent('Azure-SDK-For-Python')

        self.credentials = credentials
        self.subscription_id = subscription_id


class ManagedApplicationClient(object):
    """ARM managed applications (appliances)

    :ivar config: Configuration for client.
    :vartype config: ManagedApplicationClientConfiguration

    :ivar appliances: Appliances operations
    :vartype appliances: azure.mgmt.resource.managedapplications.operations.AppliancesOperations
    :ivar appliance_definitions: ApplianceDefinitions operations
    :vartype appliance_definitions: azure.mgmt.resource.managedapplications.operations.ApplianceDefinitionsOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = ManagedApplicationClientConfiguration(credentials, subscription_id, base_url)
        self._client = ServiceClient(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2016-09-01-preview'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.appliances = AppliancesOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.appliance_definitions = ApplianceDefinitionsOperations(
            self._client, self.config, self._serialize, self._deserialize)
