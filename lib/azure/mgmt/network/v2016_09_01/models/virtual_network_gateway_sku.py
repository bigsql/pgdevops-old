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


class VirtualNetworkGatewaySku(Model):
    """VirtualNetworkGatewaySku details.

    :param name: Gateway SKU name. Possible values are: 'Basic',
     'HighPerformance','Standard', and 'UltraPerformance'. Possible values
     include: 'Basic', 'HighPerformance', 'Standard', 'UltraPerformance'
    :type name: str or :class:`VirtualNetworkGatewaySkuName
     <azure.mgmt.network.v2016_09_01.models.VirtualNetworkGatewaySkuName>`
    :param tier: Gateway SKU tier. Possible values are: 'Basic',
     'HighPerformance','Standard', and 'UltraPerformance'. Possible values
     include: 'Basic', 'HighPerformance', 'Standard', 'UltraPerformance'
    :type tier: str or :class:`VirtualNetworkGatewaySkuTier
     <azure.mgmt.network.v2016_09_01.models.VirtualNetworkGatewaySkuTier>`
    :param capacity: The capacity.
    :type capacity: int
    """

    _validation = {
        'name': {'required': True},
        'tier': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'tier': {'key': 'tier', 'type': 'str'},
        'capacity': {'key': 'capacity', 'type': 'int'},
    }

    def __init__(self, name, tier, capacity=None):
        self.name = name
        self.tier = tier
        self.capacity = capacity
