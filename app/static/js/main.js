(function () {
    'use strict';

    var app =   angular.module('RedilApp', ['ngMaterial']);


    app.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
    }]);

    app.directive('chooseFileButton', function() {
        return {
            restrict: 'A',
            link: function (scope, elem, attrs) {
                elem.bind('click', function() {
                    angular.element(document.querySelector('#' + attrs.chooseFileButton))[0].click();
                });
            }
        };
    });

    app.directive('fileUpload', function () {
      return {
        scope: true,        //create a new scope
        link: function (scope, el, attrs) {
            el.bind('change', function (event) {
                var files = event.target.files;
                //iterate files since 'multiple' may be specified on the element
                for (var i = 0;i<files.length;i++) {
                     scope.$emit("fileSelected", { file: files[i] });
                }                                       
            });
        }
      };
    });

    app.factory("documentsFactory", ['$http', function($http) {
        var documentFactory = {};

        documentFactory.searchDocuments = function(query){
            return $http.get('/api/v1/documents', { params: { 'search_string' : query }});
        };

        return documentFactory;
    }]);

    app.controller('RedilController',['$scope', '$log', 'documentsFactory', function($scope, $log, documentsFactory) {
        $scope.results = []
        $scope.searching = false;

        $scope.searchDocuments = function() {
            console.log('en searchdocuments');
            $scope.searching = true;

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
                                    for (var i = 0; i < response.documents.length; i++) {
                                        response.documents[i].content = response.documents[i].content.replace(/\.\.\.\]/g, '...]<br>')
                                    }
                                    $scope.results = response.documents;
                                    $scope.searching = false;
                })
                                .error(function(error) {
                                    console.log(error);
                                    $scope.searching = false;

               });
              } else {
                $scope.searching = false;
                $scope.results = []
              }
            } else {
              $scope.searching = false;
              $scope.results = []
            }
        };
    }]);

    app.controller('Ctrl',['$scope', '$http','$log', function($scope, $http, $log) {
        $scope.model = {
            name: "",
            url: ""
        };

        $scope.files = [];

        $scope.$on("fileSelected", function( event, args) {
            $scope.$apply(function () {
                $scope.files.push(args.file);
            });
        });

        $scope.save = function() {
            $http({
                method: 'POST',
                url: '/upload',
                headers: {'Content-Type': undefined },
                transformRequest: function (data) {
                    var formData = new FormData();

                    formData.append("model", angular.toJson(data.model));
                    console.log(data.files);
                    console.log(data.files.length);
                    for (var i = 0; i < data.files.length; i++) {
                        formData.append("file" + i, data.files[i]);
                    }

                    return formData;
                },
                data: { model: $scope.model, files: $scope.files }
            }).success(function(data, status, headers, config) {
                console.log('success');
            }).error(function(data, status, headers, config) {
                console.log('failed');
            });
        };
    }]);
}());
