(function () {
  'use strict';

  angular.module('RedilApp', []).controller('RedilController', ['$scope', '$log', '$http', function($scope, $log, $http) {
    $scope.getResults = function() {
      $log.log("test");
      // get the URL from the input
      var userInput = $scope.input_url;
      // fire the API request
      $http.get('/api/v1/documents', { params: { 'search_string' : userInput }}).
        success(function(results) {
        $scope.results = results.documents
        $log.log(results);
      }).
      error(function(error) {
        $log.log(error);
      });
    };
  }
  ]);
}());

