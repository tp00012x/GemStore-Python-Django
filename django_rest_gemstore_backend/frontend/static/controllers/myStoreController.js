myApp.controller("myStoreController", function($scope,$http){
    $scope.gems = $http.get("/api/products/").then(
        function(response){
            $scope.gems = response.data;
        }, 
        function(error){
            $scope.error = error;
        });
});