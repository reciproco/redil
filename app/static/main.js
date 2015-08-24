(function () {
  'use strict';

  var app =   angular.module('RedilApp', []);


  app.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
  }]);

  app.factory("documents", function($http, $q) {

      var getResults = function(query){
          var canceller = $q.defer();

          var cancel = function(reason){
              canceller.resolve(reason);
          };

          var promise = $http.get('/api/v1/documents', { timeout: canceller.promise, params: { 'search_string' : query }})
                             .then(function(response) {
                                 console.log(response.data)
                                 return response.data;
                             });

          return {
              promise: promise,
              cancel: cancel
          };
      };

      return { getResults: getResults };

  });

  app.controller('RedilController', function($scope, $log, documents) {

    $scope.requests = []
    $scope.results = []

    $scope.start = function(){

      var reqlen = $scope.requests.lenght;
      for (var i = 0; i < reqlen; i++) {
          requests[i].cancel('cancelandoooo');
      }
      $scope.requests = []
      

      var request = documents.getResults($scope.input_url);
      console.log(request);
      console.log(request.promise);
      $scope.requests.push(request);
      request.promise.then(function(data){
        console.log('orimise');
        console.log(data);
        $scope.results = data.documents;
        clearRequest(request);
      }, function(reason){
        console.log(reason);
      });
    };

    $scope.cancel = function(request) {
        request.cancel('User cancelled');
        clearRequest(request);
    };

    var clearRequest = function(request){
        $scope.requests.splice($scope.requests.indexOf(request),1);
    };
 });
}());

