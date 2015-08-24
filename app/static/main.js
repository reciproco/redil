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

            documentsFactory.searchDocuments($scope.input_url)
               .success(function (response) {
                   console.log(response);
                   $scope.results = response.documents;
               })
               .error(function(error) {
                   console.log(error);

               });
        };
    }]);
}());
