from django.db import models

# Create your models here.
class Products (models.Model):
    name = models.TextField()
    price = models.FloatField()
    description = models.TextField()
    canPurchase = models.BooleanField()
    images = models.ImageField('Upload Gem Photo')

