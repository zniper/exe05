var exe05Module = angular.module('exe05', ['ui.bootstrap', 'ngCookies']);


exe05Module.config(function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
});


exe05Module.controller('LoginController', function($scope, $http, $cookies){
        $scope.login = { email: '', password: '' };
        $scope.submitForm = function() {
            if ($scope.loginForm.$valid) {
                $http.get('/authenticate?email='+$scope.login.email+'&password='+$scope.login.password).
                    success(function(data) {
                        if (data.result == 'success') {
                            $cookies.email = $scope.login.email;
                            $cookies.password = $scope.login.password;
                        } else {
                        }
                    });
            }
        }
    });

exe05Module.controller('RegisterController', function($scope, $http, $cookies, $location){
        $scope.register = { email: '', fullname: '', password: '' };
        $scope.submitForm = function() {
            if ($scope.regForm.$valid) {
                names = $scope.register.fullname.split(' ');
                var query = 'email=' + $scope.register.email + 
                            '&username=' + $scope.register.email +
                            '&first_name=' + names.splice(0, 1) +
                            '&last_name=' + names.join(' ') +
                            '&password=' + $scope.register.password +
                            '&origin=' + window.location.href;
                $location.path('/facebook/connect/?'+query).replace();
            }
        }
    });
