angular.module('bigSQL.components').controller('createNewAzureDBController', ['$scope', '$stateParams', 'PubSubService', '$rootScope', '$interval','MachineInfo', 'bamAjaxCall', '$uibModalInstance', '$uibModal', 'pgcRestApiCall', function ($scope, $stateParams, PubSubService, $rootScope, $interval, MachineInfo, bamAjaxCall, $uibModalInstance, $uibModal, pgcRestApiCall) {

    var session;
    $scope.showErrMsg = false;
    $scope.creating = false;


    $scope.loading = true;
    $scope.firstStep = true;
    $scope.secondStep = false;
    $scope.disableInsClass = true;
    $scope.days = {'Monday': 'mon', 'Tuesday': 'tue', 'Wednesday' : 'wed', 'Thursday': 'thu', 'Friday' : 'fri', 'Saturday': 'sat', 'Sunday': 'sun'};

    $scope.data = {
        'region' : 'southcentralus',
        'master_user' : '',
        'instance' : '',
        'password' : '',
        'engine_version' : '',
        'group_name' : ''
    };
    $scope.loading = false;

    /*var regions = pgcRestApiCall.getCmdData('metalist azure-regions');
    regions.then(function(data){
        $scope.loading = false;
        $scope.regions = data;
        $scope.data.region = $scope.regions[0].region;
    });*/


    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };

    $scope.createVM = function(){
        $scope.creating = true;
        $scope.showErrMsg = false;
        var data = [];
        data.push($scope.data);
        var createAzureDB = pgcRestApiCall.getCmdData('create db --params \'' + JSON.stringify(data) + '\' --cloud azure' )
        createAzureDB.then(function (data) {
            $scope.creating = false;
            if(data[0].state == 'error'){
                $scope.showErrMsg = true;
                $scope.errMsg = data[0].msg;
              }else{
                $rootScope.$emit("AzureDBCreated", data[0].msg);
                $uibModalInstance.dismiss('cancel');
              }
        })
    }


}]);