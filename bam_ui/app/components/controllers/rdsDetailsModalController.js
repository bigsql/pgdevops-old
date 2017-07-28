angular.module('bigSQL.components').controller('rdsDetailsModalController', ['$scope', '$uibModalInstance', 'PubSubService', '$rootScope', '$uibModal', 'bamAjaxCall', 'htmlMessages', function ($scope, $uibModalInstance, PubSubService, $rootScope, $uibModal, bamAjaxCall, htmlMessages) {

	var session;
	var sessPromise = PubSubService.getSession();
	var subscriptions = [];
	$scope.rdsInfo = [];
	$scope.region = $uibModalInstance.region;
	$scope.instance = $uibModalInstance.instance;
	$scope.rdsDetailsLoading = true;

	sessPromise.then(function (sessParam) {
        session = sessParam;
        session.call('com.bigsql.rdsInfo', [ $scope.region, $scope.instance]);

        session.subscribe("com.bigsql.onRdsInfo", function (data) {
            var data = JSON.parse(data[0]);
            $scope.rdsDataNotFound = false;
            if (data[0].state == "completed") {
                $scope.rdsInfo = data[0].data[0];
                $scope.rdsDetailsLoading = false;
                if (data[0].data.length < 1) {
                    $scope.rdsDataNotFound = true;
                }
                $scope.$apply();
            }
        }).then(function (subscription) {
            subscriptions.push(subscription);
        });
    });

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
        for (var i = 0; i < subscriptions.length; i++) {
            session.unsubscribe(subscriptions[i]);
        }
    };

}]);