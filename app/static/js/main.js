(function () {
    'use strict';

    var app =   angular.module('RedilApp', ['ngMaterial','ngRoute']);

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider

            .when('/', {
                templateUrl : 'static/home.html',
            })
            .when('/search', {
                templateUrl : 'static/search.html',
                controller: 'searchController'
            })
            .when('/upload', {
                templateUrl : 'static/upload.html',
                controller: 'uploadController'
            })
            .otherwise({
                redirectTo: '/'
            });

    }]);

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

    app.controller('searchController',['$scope', '$log', 'documentsFactory', function($scope, $log, documentsFactory) {
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
                console.log('Hi');
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

    app.controller('uploadController',['$scope', '$http','$log', '$timeout', function($scope, $http, $log, $timeout) {
        $scope.model = {
            name: "",
            url: ""
        };

        $scope.files = [];

        $scope.askForResults = function askForResults(jobID) {

            var timeout = "";

            var poller = function() {
                // fire another request
                $http.get('/results/'+jobID).
                    success(function(data, status, headers, config) {
                       if(status === 202) {
                           console.log(data, status);
                       } else if (status === 200){
                           console.log(data);
                           $scope.texto = data;
                           $timeout.cancel(timeout);
                           $scope.searching = false;
                           return false;
                       }
                       // continue to call the poller() function every 2 seconds
                       // until the timeout is cancelled
                       timeout = $timeout(poller, 2000);
                    });
                };
            poller();
         };


        $scope.$on("fileSelected", function( event, args) {
            $scope.$apply(function () {
                $scope.files.push(args.file);
            });
        });

        $scope.save = function() {
            $scope.searching = true;

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

                console.log(data);
                $scope.searching = false;
                //$scope.texto = decodeURIComponent(escape(window.atob((data.texto))));
                //$scope.texto = data.texto;
                $scope.askForResults(data.texto);

                console.log('success');
            }).error(function(data, status, headers, config) {
                console.log('failed');
            });
        };
    }]);

    app.controller('toolbarController',['$scope', '$http','$log','$mdDialog', function($scope, $http, $log, $mdDialog) {

        var originatorEv;

        $scope.menuitems = [ 'Search', 'Upload'];
        $scope.openMenu = function($mdOpenMenu, ev) {
            originatorEv = ev;
            $mdOpenMenu(ev);
        };
        $scope.announceClick = function(index) {
            $mdDialog.show(
                $mdDialog.alert()
                    .title('You clicked!')
                    .content('You clicked the menu item at index ' + index)
                    .ok('Nice')
            );
        };
    }]);
}());
