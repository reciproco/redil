(function () {
    'use strict';

    var app =   angular.module('RedilApp', []);


    app.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
    }]);

    app.factory("documentsFactory", ['$http', function($http) {
        var documentFactory = {};

        documentFactory.searchDocuments = function(query){
            return $http.get('/api/v1/documents', { params: { 'search_string' : query }});
        };

        return documentFactory;
    }]);

    app.controller('RedilController',['$scope', '$log', 'documentsFactory', function($scope, $log, documentsFactory) {
        $scope.results = []

        $scope.searchDocuments = function() {
            console.log('en searchdocuments');

            var parsedquery = '';

            if (typeof $scope.input_url != 'undefined') {
              var query = $scope.input_url.match(/("[^"]+"|[^"\s]+)/g);
              console.log(query);
              var ql = query.length;
              for (var i = 0; i < ql; i++) {
                if(query[i].length > 2) {
                  parsedquery = parsedquery + query[i] + ' ';
                }
              }
              if (parsedquery.length > 2) {
                console.log(parsedquery);
                documentsFactory.searchDocuments(parsedquery)
                                .success(function (response) {
                                    console.log(response);
                                    $scope.results = response.documents;
                })
                                .error(function(error) {
                                    console.log(error);

               });
              } else {
                $scope.results = []
              }
            } else {
              $scope.results = []
            }
        };
    }]);
}());
