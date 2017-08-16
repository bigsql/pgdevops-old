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


class MonitoringPolicyDescription(Model):
    """Describes the parameters for monitoring an upgrade in Monitored mode.

    :param failure_action: Possible values include: 'Invalid', 'Rollback',
     'Manual'
    :type failure_action: str
    :param health_check_wait_duration_in_milliseconds:
    :type health_check_wait_duration_in_milliseconds: str
    :param health_check_stable_duration_in_milliseconds:
    :type health_check_stable_duration_in_milliseconds: str
    :param health_check_retry_timeout_in_milliseconds:
    :type health_check_retry_timeout_in_milliseconds: str
    :param upgrade_timeout_in_milliseconds:
    :type upgrade_timeout_in_milliseconds: str
    :param upgrade_domain_timeout_in_milliseconds:
    :type upgrade_domain_timeout_in_milliseconds: str
    """ 

    _attribute_map = {
        'failure_action': {'key': 'FailureAction', 'type': 'str'},
        'health_check_wait_duration_in_milliseconds': {'key': 'HealthCheckWaitDurationInMilliseconds', 'type': 'str'},
        'health_check_stable_duration_in_milliseconds': {'key': 'HealthCheckStableDurationInMilliseconds', 'type': 'str'},
        'health_check_retry_timeout_in_milliseconds': {'key': 'HealthCheckRetryTimeoutInMilliseconds', 'type': 'str'},
        'upgrade_timeout_in_milliseconds': {'key': 'UpgradeTimeoutInMilliseconds', 'type': 'str'},
        'upgrade_domain_timeout_in_milliseconds': {'key': 'UpgradeDomainTimeoutInMilliseconds', 'type': 'str'},
    }

    def __init__(self, failure_action=None, health_check_wait_duration_in_milliseconds=None, health_check_stable_duration_in_milliseconds=None, health_check_retry_timeout_in_milliseconds=None, upgrade_timeout_in_milliseconds=None, upgrade_domain_timeout_in_milliseconds=None):
        self.failure_action = failure_action
        self.health_check_wait_duration_in_milliseconds = health_check_wait_duration_in_milliseconds
        self.health_check_stable_duration_in_milliseconds = health_check_stable_duration_in_milliseconds
        self.health_check_retry_timeout_in_milliseconds = health_check_retry_timeout_in_milliseconds
        self.upgrade_timeout_in_milliseconds = upgrade_timeout_in_milliseconds
        self.upgrade_domain_timeout_in_milliseconds = upgrade_domain_timeout_in_milliseconds
