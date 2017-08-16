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

from .partition_scheme_description import PartitionSchemeDescription


class NamedPartitionSchemeDescription(PartitionSchemeDescription):
    """Describes the named partition scheme of the service.

    :param PartitionScheme: Polymorphic Discriminator
    :type PartitionScheme: str
    :param count: The number of partitions.
    :type count: int
    :param names: Array of size specified by the ‘Count’ parameter, for the
     names of the partitions.
    :type names: list of str
    """ 

    _validation = {
        'PartitionScheme': {'required': True},
        'count': {'required': True},
        'names': {'required': True},
    }

    _attribute_map = {
        'PartitionScheme': {'key': 'PartitionScheme', 'type': 'str'},
        'count': {'key': 'Count', 'type': 'int'},
        'names': {'key': 'Names', 'type': '[str]'},
    }

    def __init__(self, count, names):
        super(NamedPartitionSchemeDescription, self).__init__()
        self.count = count
        self.names = names
        self.PartitionScheme = 'Named'
