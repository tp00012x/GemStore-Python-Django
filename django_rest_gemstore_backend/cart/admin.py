from django.contrib import admin

# Register your models here.
from cart.models import Cart, ProductOrder

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'order_date')

admin.site.register(ProductOrder, ProductAdmin)
admin.site.register(Cart,CartAdmin)