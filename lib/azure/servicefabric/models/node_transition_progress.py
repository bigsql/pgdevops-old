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


class NodeTransitionProgress(Model):
    """Information about an NodeTransition operation.  This class contains an
    OperationState and a NodeTransitionResult.  The NodeTransitionResult is
    not valid until OperationState
    is Completed or Faulted.
    .

    :param state: Possible values include: 'Invalid', 'Running',
     'RollingBack', 'Completed', 'Faulted', 'Cancelled', 'ForceCancelled'
    :type state: str
    :param node_transition_result:
    :type node_transition_result: :class:`NodeTransitionResult
     <azure.servicefabric.models.NodeTransitionResult>`
    """ 

    _attribute_map = {
        'state': {'key': 'State', 'type': 'str'},
        'node_transition_result': {'key': 'NodeTransitionResult', 'type': 'NodeTransitionResult'},
    }

    def __init__(self, state=None, node_transition_result=None):
        self.state = state
        self.node_transition_result = node_transition_result
