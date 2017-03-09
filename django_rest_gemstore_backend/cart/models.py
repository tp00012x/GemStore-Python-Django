from django.db import models
from django.contrib.auth.models import User
from products.models import Products
from decimal import Decimal

# Create your models here.

class Cart (models.Model):
    user = models.ForeignKey(User)
    active = models.BooleanField(default =True)
    order_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=100,null=True)
    payment_id = models.CharField(max_length=100, null=True)

    def add_to_cart(self,products_id):
        product = Products.objects.get(pk=products_id)
        try:
            preexisting_order =ProductOrder.objects.get(product_id=product.id,
                                                        cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except ProductOrder.DoesNotExist:
            new_order = ProductOrder.objects.create(
                product_id = product.id,
                cart = self,
                quantity = 1
            )
            new_order.save()
    def remove_from_cart(self,products_id):
        product = Products.objects.get(pk=products_id)
        try:
            preexisiting_order = ProductOrder.objects.get(product_id=product.id,cart=self)
            if preexisiting_order.quantity > 1:
                preexisiting_order.quantity -= 1
                preexisiting_order.save()
            else:
                preexisiting_order.delete()
        except ProductOrder.DoesNotExist:
            pass


class ProductOrder(models.Model):
    product = models.ForeignKey(Products)
    cart = models.ForeignKey(Cart)
    quantity = models.IntegerField()