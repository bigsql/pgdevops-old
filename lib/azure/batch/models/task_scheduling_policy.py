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


class TaskSchedulingPolicy(Model):
    """Specifies how tasks should be distributed across compute nodes.

    :param node_fill_type: How tasks should be distributed across compute
     nodes. Possible values include: 'spread', 'pack'
    :type node_fill_type: str or :class:`ComputeNodeFillType
     <azure.batch.models.ComputeNodeFillType>`
    """

    _validation = {
        'node_fill_type': {'required': True},
    }

    _attribute_map = {
        'node_fill_type': {'key': 'nodeFillType', 'type': 'ComputeNodeFillType'},
    }

    def __init__(self, node_fill_type):
        self.node_fill_type = node_fill_type
