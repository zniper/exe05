var exe05Module = angular.module('exe05', ['ui.bootstrap', 'ngCookies']);


exe05Module.config(function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
});

exe05Module.controller('LoginController', function($scope, $http, $cookies, $location){
        $scope.login = { email: '', password: '' };
        $scope.submitForm = function() {
            if ($scope.loginForm.$valid) {
                $http.get('/authenticate/' +
                          '?email=' + $scope.login.email+
                          '&password=' + $scope.login.password).
                    success(function(data) {
                        if (data.result == 'success') {
                            setCredentials(data.uid, data.token);
                            goNext();
                        } else {
                            $scope.showAlert = true;
                        }
                    });
            }
        }
        
        var setCredentials = function(uid, token) {
            $cookies.uid = uid;
            $cookies.token = token;
        }

        var goNext = function() {
            // ughh, a little non-angularjs
            var path = window.location.pathname.split('/');
            path = path.splice(0, path.length-1).join('/') + '/friends.html';
            window.location.pathname = path;
        }

        var init = function() {
            params = $location.search();
            if (params.res=='1' && params.token.length>0) {
                // try to check authentication
                // then move to the friend list editing
                setCredentials(params.uid, params.token);
                goNext();
            } else if (params.res=='0') {
                alert('Registration Failed. Please verify your information and try again.');
            }
        };

        init();

    });

exe05Module.controller('RegisterController', function($scope, $http, $cookies, $location){
        $scope.register = { email: '', fullname: '', password: '', ref: $location.absUrl() };
        $scope.submitForm = function() {
        }
    });


exe05Module.controller('FriendListController', function($scope, $http, $cookies) {

        $scope.updateName = function(index) {
            data = $scope.friends[index];
            config = {headers: {'X-CSRFToken': $cookies.csrftoken }};
            $http.put('/contacts/' + data.id, data, config).
                success(function(data, status) {
                    if (status == 200) {
                        alert('Done!');
                    } 
                });
        }

        var getFriendlist = function() {
            $http.get('/users/'+$cookies.uid+'/friends/'+'?token='+$cookies.token).
                success(function(data, status) {
                    if (status == 200) {
                        $scope.friends = data;
                    } else {
                        // nothing
                    }
                });
        }

        var init = function() {
            getFriendlist();
        };

        init();
    });


exe05Module.controller('ProfileController', function($scope, $http, $cookies) {

        var getProfile= function() {
            $http.get('/users/'+$cookies.uid+'?token='+$cookies.token).
                success(function(data, status) {
                    if (status == 200) {
                        $scope.fn = data['first_name'];
                        $scope.ln = data['last_name'];
                        delete data['first_name'];
                        delete data['last_name'];
                        $scope.profile = data;
                    } else {
                        // nothing
                    }
                });
        }

        var init = function() {
            getProfile();
        };

        init();
    });

exe05Module.controller('NavigationController', function($scope, $http, $cookies) {

        var backHome = function() {
            var path = window.location.pathname.split('/');
            path = path.splice(0, path.length-1).join('/') + '/index.html';
            window.location.pathname = path;
        };

        $scope.logOut= function() {
            delete $cookies.uid;
            delete $cookies.token;
            delete $cookies.sessionid;
            delete $cookies.csrftoken;
            backHome();
        };

        var init = function() {
            if (!$cookies.token) {
                backHome();
            };
        };

        init();

    });
