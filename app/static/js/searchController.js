redil.controller('searchController',['$scope', '$log', 'documentsFactory', function($scope, $log, documentsFactory) {
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
