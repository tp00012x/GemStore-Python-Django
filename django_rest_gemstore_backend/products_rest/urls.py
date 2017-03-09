from django.conf.urls import url, include
from rest_framework import routers
from products_rest.viewsets import ProductsViewSet

router = routers.DefaultRouter()
router.register('products', ProductsViewSet, 'products')

urlpatterns = [
    url(r'^', include(router.urls))  # base router
]
