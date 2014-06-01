var exe05 = angular.module('exe05', [
    'ngRoute',
    'exe05Controllers'
]);

exe05.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/login', {
                templateUrl: 'partials/login.html',
                controller: 'LoginController'
            }).
            when('/friends', {
                templateUrl: 'partials/friends.html',
                controller: 'FriendListController'
            }).
            otherwise({
                redirectTo: '/login'
            });
    }]);
