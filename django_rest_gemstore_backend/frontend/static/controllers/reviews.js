var reviewsModule = angular.module('storeReviews', [])

angular.module('storeReviews').directive('reviews', function(){
    return {
        restrict: 'A',
        templateUrl: 'static/templates/reviews.html'
    }
})

reviewsModule.controller('myReviewsController', function($http){
    this.reviews = {}

    this.addReview = function(product){

        $http.post('/api/reviews/', this.reviews).then(function(data){
            console.log("Successful submission")
        }).catch(function(data){
            console.log("Unsuccessful submission")
        })

        if(!product.reviews)
            product.reviews =[]

        //  product.reviews.push(this.reviews)
            this.reviews = {}
    }

    this.validate = function(){
        this.reviewForm.comments.$setDirty();
        this.reviewForm.email.$setDirty();
        this.reviewForm.rating.$setDirty();
    }
})