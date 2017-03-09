from django.db import models

# Create your models here.
class reviews (models.Model):
    stars = models.IntegerField()
    body = models.TextField()
    author = models.EmailField()