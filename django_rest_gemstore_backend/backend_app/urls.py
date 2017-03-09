"""django_rest_gemstore_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from frontend.views import index, add_to_cart, remove_from_cart, cart, checkout, process_order, order_error, complete_order

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/',include ('products_rest.urls', namespace='api')),
    url(r'^api/',include ('reviews_rest.reviews_urls', namespace='api')),
    url(r'^$', index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^add/(\d+)', add_to_cart, name='add_to_cart'),
    url(r'^remove/(\d+)', remove_from_cart, name='remove_from_cart'),
    url(r'^cart/', cart,name='cart'),
    url(r'^checkout/(\w+)', checkout, name='checkout'),
    url(r'^process/(\w+)', process_order, name='process_order'),
    url(r'^order_error/(\w+)', order_error, name='order_error'),
    url(r'^complete_order/(\w+)', complete_order, name='complete_order'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()