angular.module('bigSQL.components').controller('bamLoading', ['$scope', 'PubSubService', '$rootScope', '$window', '$timeout', 'bamAjaxCall', function ($scope, PubSubService, $rootScope, $window, $timeout, bamAjaxCall) {

	$scope.bamLoading = true;
	var subscriptions = [];
	var session;

  var sessPromise = PubSubService.getSession();
  sessPromise.then(function (sessPram) {
  	session = sessPram;
  	session.call('com.bigsql.serverStatus');
      session.subscribe("com.bigsql.onServerStatus", function (args) {
      	$scope.bamLoading = false;
        $window.location.href = "#/"
        $scope.$apply();
   			var components = $(JSON.parse(args[0])).filter(function(i,n){ return n.category === 1;});
    		if(components.length != 0){
    			$scope.pgComp = components;
    		}
    }).then(function (subscription) {
        subscriptions.push(subscription);
    });
  });

	$timeout(function() {
        if ($scope.bamLoading) {
            $window.location.reload();
        };
    }, 10000);

	$scope.$on('$destroy', function () {
        for (var i = 0; i < subscriptions.length; i++) {
            session.unsubscribe(subscriptions[i]);
        }
    });

}]);