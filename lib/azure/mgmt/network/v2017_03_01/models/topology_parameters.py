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


class TopologyParameters(Model):
    """Parameters that define the representation of topology.

    :param target_resource_group_name: The name of the target resource group
     to perform topology on.
    :type target_resource_group_name: str
    """

    _validation = {
        'target_resource_group_name': {'required': True},
    }

    _attribute_map = {
        'target_resource_group_name': {'key': 'targetResourceGroupName', 'type': 'str'},
    }

    def __init__(self, target_resource_group_name):
        self.target_resource_group_name = target_resource_group_name
