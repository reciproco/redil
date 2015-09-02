redil.factory("documentsFactory", ['$http', function($http) {
    var documentFactory = {};

    documentFactory.searchDocuments = function(query){
        return $http.get('/api/v1/documents', { params: { 'search_string' : query }});
    };

    return documentFactory;
}]);
