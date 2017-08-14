angular.module('bigSQL.components').controller('credentialManagerController', ['$rootScope', '$scope', '$uibModal','PubSubService', 'MachineInfo', 'UpdateComponentsService', 'bamAjaxCall', '$window', '$cookies', '$sce', 'htmlMessages', '$timeout', function ($rootScope, $scope, $uibModal, PubSubService, MachineInfo, UpdateComponentsService, bamAjaxCall, $window, $cookies, $sce, htmlMessages, $timeout) {

	$scope.alerts = [];
	$scope.loading = true;
	$scope.types = {'SSH Key' : 'ssh-key', 'Cloud' : 'cloud', 'Password' : 'pwd'};
	// $scope.cloudTypes = {'AWS': 'AWS', 'Azure': 'Azure'};
	
	$scope.data = {
		'type' : '',
		'credential_name' : '',
		'user' : '',
		'password' : '',
		'ssh_key' : '',
		'cloud_key' : '',
		'ssh_sudo_pwd' : '',
		'cloud_name' : 'AWS',
		'cloud_secret' : '',
		'region' : ''
	}


	var credentialsList = function(argument) {
		$scope.isAllSelected = false;
		var getCredentials = bamAjaxCall.getCmdData('pgc/credentials/list/')
		getCredentials.then(function (data) {
			$scope.loading = false;
			$scope.credentialsList = JSON.parse(data[0]);
			for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
				$scope.credentialsList[i].selected = false;
			}
			if ($scope.credentialsList.length == 0) {
				$scope.noCredMsg = $sce.trustAsHtml(htmlMessages.getMessage('no-credentials'));
			}
		})

	}

	var regions = bamAjaxCall.getCmdData('metalist/aws-regions');
    regions.then(function(data){
        $scope.loading = false;
        $scope.regions = data;
        $scope.data.region = $scope.regions[0].region;
    });

	$rootScope.$on('refreshCreds', function (argument) {
		credentialsList();
	});

	credentialsList();

	$scope.addCredential = function () {
		var addCred = bamAjaxCall.postData('/api/pgc/credentials/create/', $scope.data)
		addCred.then(function (data) {
			var parseData = JSON.parse(data[0]);
			if (parseData[0].state=='info') {
				$scope.alerts.push({
                    msg: data,
                    type: 'success'
                });
			}else{
				$scope.alerts.push({
                    msg: data,
                    type: 'error'
                });
			}
		})
	}

	$scope.toggleAll = function() { 
        if($scope.isAllSelected){
            $scope.isAllSelected = false;
        }else{
            $scope.isAllSelected = true;
        }
        angular.forEach($scope.credentialsList, function(itm){ itm.selected = $scope.isAllSelected; });
    }

    $scope.optionToggled = function(name){
    	console.log($scope.credentialsList);
    }

    $scope.checkOptions = function (argument) {
    	$scope.showUpdate = false;
    	$scope.showDeleteUsageReport = false;
    	var selectedCreds = [];
    	for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
			if($scope.credentialsList[i].selected){
				selectedCreds.push($scope.credentialsList[i]);
			}
		}
		if (selectedCreds.length==0) {
			$scope.showDeleteUsageReport = false;
			$scope.showUpdate = false;
		}else if(selectedCreds.length == 1){
			$scope.showUpdate = true;
			$scope.showDeleteUsageReport = true;
		}else{
			$scope.showDeleteUsageReport = true;
		}
    }

	$scope.deleteCredential = function (cred_uuid) {
		var selectedCreds = [];
		for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
			if($scope.credentialsList[i].selected){
				selectedCreds.push($scope.credentialsList[i]);
			}
		}
		if (selectedCreds.length>0) {
			var cred_uuids = [];
			for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
				if($scope.credentialsList[i].selected){
					cred_uuids.push($scope.credentialsList[i].cred_uuid);
				}
			}
			var modalInstance = $uibModal.open({
	            templateUrl: '../app/components/partials/confirmDeletionModal.html',
	            controller: 'confirmDeletionModalController',
	        });
	        modalInstance.deleteFiles = cred_uuids;
	        modalInstance.comp = 'credentials';
	        modalInstance.deleteCred = true;
		}else{
			$scope.alerts.push({
				msg: htmlMessages.getMessage('select-one-cred'),
                type: 'warning'
            });
		}
	}

	$scope.addCred = function (title) {
		var modalInstance = $uibModal.open({
                templateUrl: '../app/components/partials/addCredentialModal.html',
                controller: 'addCredentialModalController',
                keyboard  : false,
                backdrop  : 'static',
            });
		modalInstance.title = title;
	}

	$scope.updateCred = function (title, type) {
		var updateCreds = [];
		for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
			if($scope.credentialsList[i].selected){
				updateCreds.push($scope.credentialsList[i]);
			}
		}
		if (updateCreds.length == 1) {
			var modalInstance = $uibModal.open({
                templateUrl: '../app/components/partials/addCredentialModal.html',
                controller: 'addCredentialModalController',
                keyboard  : false,
                backdrop  : 'static',
            });
			modalInstance.title = title;
			modalInstance.updateCred = updateCreds;
			modalInstance.type = type;
		}
	}

	$scope.openUsage = function (name, host_list, cred_type) {
		var selectedCreds = [];
		for (var i = $scope.credentialsList.length - 1; i >= 0; i--) {
			if($scope.credentialsList[i].selected){
				selectedCreds.push($scope.credentialsList[i]);
			}
		}
		if (name || selectedCreds.length>0) {
			var modalInstance = $uibModal.open({
                templateUrl: '../app/components/partials/credentialUsage.html',
                controller: 'credentialUsageController',
                keyboard  : false,
                backdrop  : 'static',
            });
			modalInstance.name = name;
			modalInstance.cred_list = host_list;
			modalInstance.cred_type = cred_type;
			modalInstance.selectedCreds = selectedCreds;
		}else{
			$scope.alerts.push({
				msg: htmlMessages.getMessage('select-one-cred'),
                type: 'warning'
            });
		}
	}

	$scope.closeAlert = function (index) {
	    $scope.alerts.splice(index, 1);
	};

}]);