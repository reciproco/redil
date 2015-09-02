redil.config(['$routeProvider', function($routeProvider) {
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
