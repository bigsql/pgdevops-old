angular.module('bigSQL.components').controller('ComponentsSettingsController', ['$rootScope', '$scope', '$uibModal', 'PubSubService', 'MachineInfo', 'UpdateComponentsService', '$window', 'bamAjaxCall', function ($rootScope, $scope, $uibModal, PubSubService, MachineInfo, UpdateComponentsService, $window, bamAjaxCall) {
    $scope.alerts = [];

    var session;
    var subscriptions = [];
    $scope.updateSettings;
    $scope.components = {};
    $scope.settingsOptions = [{name:'Weekly'},{name:'Daily'},{name:'Monthly'}]

    $scope.open = function (manual) {
        UpdateComponentsService.set('');
        if (manual == "manual") {
            UpdateComponentsService.setCheckUpdatesManual();
        } else {
            UpdateComponentsService.setCheckUpdatesAuto();
        }

        var modalInstance = $uibModal.open({
            templateUrl: '../app/components/partials/updateModal.html',
            windowClass: 'bam-update-modal modal',
            controller: 'ComponentsUpdateController',
        });
    };

    var infoData = bamAjaxCall.getCmdData('info')
    infoData.then(function(data) {
        $scope.pgcInfo = data[0];
        if (data[0].last_update_utc) {
            $scope.lastUpdateStatus = new Date(data[0].last_update_utc.replace(/-/g, '/') + " UTC").toString().split(' ',[5]).splice(1).join(' ');
        }
        if (MachineInfo.getUpdationMode() == "manual") {
            $scope.settingType = 'manual';
        } else {
            $scope.settingType = 'auto';
            session.call('com.bigsql.get_host_settings');
        }

    });

    var sessionPromise = PubSubService.getSession();
    sessionPromise.then(function (val) {
        $rootScope.$emit('topMenuEvent');
        session = val;
        
        $scope.updateManualSettings = function () {
            session.call('com.bigsql.update_host_settings', ['localhost', "None", '']).then(
                function (subscription) {
                    session.call('com.bigsql.get_host_settings').then(
                        function (sub) {
                            MachineInfo.setUpdationMode(sub);
                            var data = "Update settings has been set to Manual";
                            $scope.alerts.push({
                                msg: data
                            });
                            $scope.$apply();
                        });
                });
        };

        $scope.onAutomaticOptionSelection = function (value) {
            session.call('com.bigsql.update_host_settings', ['localhost', $scope.automaticSettings.name, '']).then(
                function (subscription) {
                    session.call('com.bigsql.get_host_settings').then(
                        function (sub) {
                            MachineInfo.setUpdationMode(sub);
                            var data = "Update settings has been set to " + sub.interval + ", next update is on " + sub.next_update_utc;
                            $scope.alerts.push({
                                msg: data
                            });
                            $scope.$apply();
                        });
                });
        };

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

    });


    /**
     Unsubscribe to all the apis on the template and scope destroy
     **/
    $scope.$on('$destroy', function () {
        for (var i = 0; i < subscriptions.length; i++) {
            session.unsubscribe(subscriptions[i]);
        }

    });

}]);