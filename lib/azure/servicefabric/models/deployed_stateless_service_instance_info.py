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

from .deployed_service_replica_info import DeployedServiceReplicaInfo


class DeployedStatelessServiceInstanceInfo(DeployedServiceReplicaInfo):
    """Information about a stateless service instance deployed on a node.

    :param service_name: Full hierarchical name of the service in URI format
     starting with `fabric:`.
    :type service_name: str
    :param service_type_name: Name of the service type as specified in the
     service manifest.
    :type service_type_name: str
    :param service_manifest_name: The name of the service manifest in which
     this service type is defined.
    :type service_manifest_name: str
    :param code_package_name: The name of the code package that hosts this
     replica.
    :type code_package_name: str
    :param partition_id:
    :type partition_id: str
    :param replica_status: Possible values include: 'Invalid', 'InBuild',
     'Standby', 'Ready', 'Down', 'Dropped'
    :type replica_status: str
    :param address: The last address returned by the replica in Open or
     ChangeRole.
    :type address: str
    :param service_package_activation_id:
    :type service_package_activation_id: str
    :param ServiceKind: Polymorphic Discriminator
    :type ServiceKind: str
    :param instance_id: Id of the stateless service instance.
    :type instance_id: str
    """ 

    _validation = {
        'ServiceKind': {'required': True},
    }

    _attribute_map = {
        'service_name': {'key': 'ServiceName', 'type': 'str'},
        'service_type_name': {'key': 'ServiceTypeName', 'type': 'str'},
        'service_manifest_name': {'key': 'ServiceManifestName', 'type': 'str'},
        'code_package_name': {'key': 'CodePackageName', 'type': 'str'},
        'partition_id': {'key': 'PartitionID', 'type': 'str'},
        'replica_status': {'key': 'ReplicaStatus', 'type': 'str'},
        'address': {'key': 'Address', 'type': 'str'},
        'service_package_activation_id': {'key': 'ServicePackageActivationId', 'type': 'str'},
        'ServiceKind': {'key': 'ServiceKind', 'type': 'str'},
        'instance_id': {'key': 'InstanceId', 'type': 'str'},
    }

    def __init__(self, service_name=None, service_type_name=None, service_manifest_name=None, code_package_name=None, partition_id=None, replica_status=None, address=None, service_package_activation_id=None, instance_id=None):
        super(DeployedStatelessServiceInstanceInfo, self).__init__(service_name=service_name, service_type_name=service_type_name, service_manifest_name=service_manifest_name, code_package_name=code_package_name, partition_id=partition_id, replica_status=replica_status, address=address, service_package_activation_id=service_package_activation_id)
        self.instance_id = instance_id
        self.ServiceKind = 'Stateless'
