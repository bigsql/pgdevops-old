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

from .partition_safety_check import PartitionSafetyCheck


class WaitForPrimarySwapSafetyCheck(PartitionSafetyCheck):
    """Safety check that waits for the primary replica to be moved out of the
    node before starting an upgrade to ensure the avaiability of the primary
    replica for the partition.

    :param Kind: Polymorphic Discriminator
    :type Kind: str
    :param partition_id: Id of the partition which is undergoing the safety
     check.
    :type partition_id: str
    """ 

    _validation = {
        'Kind': {'required': True},
    }

    def __init__(self, partition_id=None):
        super(WaitForPrimarySwapSafetyCheck, self).__init__(partition_id=partition_id)
        self.Kind = 'WaitForPrimarySwap'
