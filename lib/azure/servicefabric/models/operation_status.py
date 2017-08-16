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


class OperationStatus(Model):
    """Contains the OperationId, OperationState, and OperationType for
    user-induced operations.

    :param operation_id:
    :type operation_id: str
    :param state: Possible values include: 'Invalid', 'Running',
     'RollingBack', 'Completed', 'Faulted', 'Cancelled', 'ForceCancelled'
    :type state: str
    :param type: Possible values include: 'invalid', 'partitionDataLoss',
     'partitionQuorumLoss', 'partitionRestart', 'nodeTransition'
    :type type: str
    """ 

    _attribute_map = {
        'operation_id': {'key': 'OperationId', 'type': 'str'},
        'state': {'key': 'State', 'type': 'str'},
        'type': {'key': 'Type', 'type': 'str'},
    }

    def __init__(self, operation_id=None, state=None, type=None):
        self.operation_id = operation_id
        self.state = state
        self.type = type
