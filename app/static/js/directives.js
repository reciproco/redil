redil.directive('chooseFileButton', function() {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            elem.bind('click', function() {
                angular.element(document.querySelector('#' + attrs.chooseFileButton))[0].click();
            });
        }
    };
});

redil.directive('fileUpload', function () {
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
