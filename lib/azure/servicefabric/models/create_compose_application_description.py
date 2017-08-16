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

from msrest.serialization import Model


class CreateComposeApplicationDescription(Model):
    """Defines description for creating a Service Fabric compose application.
    .

    :param application_name:
    :type application_name: str
    :param compose_file_content: The content of the compose file that
     describes application to create.
    :type compose_file_content: str
    :param repository_credential:
    :type repository_credential: :class:`RepositoryCredential
     <azure.servicefabric.models.RepositoryCredential>`
    """ 

    _validation = {
        'application_name': {'required': True},
        'compose_file_content': {'required': True},
    }

    _attribute_map = {
        'application_name': {'key': 'ApplicationName', 'type': 'str'},
        'compose_file_content': {'key': 'ComposeFileContent', 'type': 'str'},
        'repository_credential': {'key': 'RepositoryCredential', 'type': 'RepositoryCredential'},
    }

    def __init__(self, application_name, compose_file_content, repository_credential=None):
        self.application_name = application_name
        self.compose_file_content = compose_file_content
        self.repository_credential = repository_credential
