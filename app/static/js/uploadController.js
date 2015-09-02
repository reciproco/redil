redil.controller('uploadController',['$scope', '$http','$log', '$timeout', function($scope, $http, $log, $timeout) {
    $scope.model = {
        name: "",
        url: ""
    };

    $scope.files = [];
    $scope.jobs = [];

    $scope.askForResults = function askForResults(jobID) {

        var timeout = "";

        var poller = function() {
            $http.get('/results/'+jobID).
                  success(function(data, status, headers, config) {
                      if(status === 202) {
                          console.log(data, status);
                      } else if (status === 200){
                          console.log(data);
                          $scope.jobs.push(data);
                          $timeout.cancel(timeout);
                          $scope.searching = false;
                          return false;
                      }
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
        $scope.jobs = [];

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

                return formData; },
            data: { model: $scope.model, files: $scope.files }
        }).success(function(data, status, headers, config) {
            console.log(data);

            for (var i=0; i < data.job_ids.length; i++) {
               $scope.askForResults(data.job_ids[i]);
            }
            angular.element(document.querySelector('#file-input')).val(null);
            $scope.files = [];
            console.log('success');
        }).error(function(data, status, headers, config) {
            $scope.searching = false;
            console.log('failed');
        });
    };
}]);
