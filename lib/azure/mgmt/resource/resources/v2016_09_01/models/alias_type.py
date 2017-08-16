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


class AliasType(Model):
    """The alias type. .

    :param name: The alias name.
    :type name: str
    :param paths: The paths for an alias.
    :type paths: list of :class:`AliasPathType
     <azure.mgmt.resource.resources.v2016_09_01.models.AliasPathType>`
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'paths': {'key': 'paths', 'type': '[AliasPathType]'},
    }

    def __init__(self, name=None, paths=None):
        self.name = name
        self.paths = paths
