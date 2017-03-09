from django.conf.urls import url,include
from rest_framework import routers
from reviews_rest.reviews_viewsets import reviews_viewsets

router  = routers.DefaultRouter()
router.register('reviews', reviews_viewsets,'reviews')

urlpatterns = [
    url(r'^', include(router.urls))
]