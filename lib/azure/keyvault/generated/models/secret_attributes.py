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

from .attributes import Attributes


class SecretAttributes(Attributes):
    """The secret management attributes.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param enabled: Determines whether the object is enabled.
    :type enabled: bool
    :param not_before: Not before date in UTC.
    :type not_before: datetime
    :param expires: Expiry date in UTC.
    :type expires: datetime
    :ivar created: Creation time in UTC.
    :vartype created: datetime
    :ivar updated: Last updated time in UTC.
    :vartype updated: datetime
    """

    _validation = {
        'created': {'readonly': True},
        'updated': {'readonly': True},
    }

    def __init__(self, enabled=None, not_before=None, expires=None):
        super(SecretAttributes, self).__init__(enabled=enabled, not_before=not_before, expires=expires)
