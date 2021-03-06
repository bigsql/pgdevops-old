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

from .resource import Resource


class BackupItem(Resource):
    """Backup description.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Resource Id.
    :vartype id: str
    :param name: Resource Name.
    :type name: str
    :param kind: Kind of resource.
    :type kind: str
    :param location: Resource Location.
    :type location: str
    :param type: Resource type.
    :type type: str
    :param tags: Resource tags.
    :type tags: dict
    :ivar backup_id: Id of the backup.
    :vartype backup_id: int
    :ivar storage_account_url: SAS URL for the storage account container which
     contains this backup.
    :vartype storage_account_url: str
    :ivar blob_name: Name of the blob which contains data for this backup.
    :vartype blob_name: str
    :ivar backup_item_name: Name of this backup.
    :vartype backup_item_name: str
    :ivar status: Backup status. Possible values include: 'InProgress',
     'Failed', 'Succeeded', 'TimedOut', 'Created', 'Skipped',
     'PartiallySucceeded', 'DeleteInProgress', 'DeleteFailed', 'Deleted'
    :vartype status: str or :class:`BackupItemStatus
     <azure.mgmt.web.models.BackupItemStatus>`
    :ivar size_in_bytes: Size of the backup in bytes.
    :vartype size_in_bytes: long
    :ivar created: Timestamp of the backup creation.
    :vartype created: datetime
    :ivar log: Details regarding this backup. Might contain an error message.
    :vartype log: str
    :ivar databases: List of databases included in the backup.
    :vartype databases: list of :class:`DatabaseBackupSetting
     <azure.mgmt.web.models.DatabaseBackupSetting>`
    :ivar scheduled: True if this backup has been created due to a schedule
     being triggered.
    :vartype scheduled: bool
    :ivar last_restore_time_stamp: Timestamp of a last restore operation which
     used this backup.
    :vartype last_restore_time_stamp: datetime
    :ivar finished_time_stamp: Timestamp when this backup finished.
    :vartype finished_time_stamp: datetime
    :ivar correlation_id: Unique correlation identifier. Please use this along
     with the timestamp while communicating with Azure support.
    :vartype correlation_id: str
    :ivar website_size_in_bytes: Size of the original web app which has been
     backed up.
    :vartype website_size_in_bytes: long
    """

    _validation = {
        'id': {'readonly': True},
        'location': {'required': True},
        'backup_id': {'readonly': True},
        'storage_account_url': {'readonly': True},
        'blob_name': {'readonly': True},
        'backup_item_name': {'readonly': True},
        'status': {'readonly': True},
        'size_in_bytes': {'readonly': True},
        'created': {'readonly': True},
        'log': {'readonly': True},
        'databases': {'readonly': True},
        'scheduled': {'readonly': True},
        'last_restore_time_stamp': {'readonly': True},
        'finished_time_stamp': {'readonly': True},
        'correlation_id': {'readonly': True},
        'website_size_in_bytes': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'kind': {'key': 'kind', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'backup_id': {'key': 'properties.id', 'type': 'int'},
        'storage_account_url': {'key': 'properties.storageAccountUrl', 'type': 'str'},
        'blob_name': {'key': 'properties.blobName', 'type': 'str'},
        'backup_item_name': {'key': 'properties.name', 'type': 'str'},
        'status': {'key': 'properties.status', 'type': 'BackupItemStatus'},
        'size_in_bytes': {'key': 'properties.sizeInBytes', 'type': 'long'},
        'created': {'key': 'properties.created', 'type': 'iso-8601'},
        'log': {'key': 'properties.log', 'type': 'str'},
        'databases': {'key': 'properties.databases', 'type': '[DatabaseBackupSetting]'},
        'scheduled': {'key': 'properties.scheduled', 'type': 'bool'},
        'last_restore_time_stamp': {'key': 'properties.lastRestoreTimeStamp', 'type': 'iso-8601'},
        'finished_time_stamp': {'key': 'properties.finishedTimeStamp', 'type': 'iso-8601'},
        'correlation_id': {'key': 'properties.correlationId', 'type': 'str'},
        'website_size_in_bytes': {'key': 'properties.websiteSizeInBytes', 'type': 'long'},
    }

    def __init__(self, location, name=None, kind=None, type=None, tags=None):
        super(BackupItem, self).__init__(name=name, kind=kind, location=location, type=type, tags=tags)
        self.backup_id = None
        self.storage_account_url = None
        self.blob_name = None
        self.backup_item_name = None
        self.status = None
        self.size_in_bytes = None
        self.created = None
        self.log = None
        self.databases = None
        self.scheduled = None
        self.last_restore_time_stamp = None
        self.finished_time_stamp = None
        self.correlation_id = None
        self.website_size_in_bytes = None
