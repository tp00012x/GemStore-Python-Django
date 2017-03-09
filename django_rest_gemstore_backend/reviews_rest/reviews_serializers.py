from rest_framework import serializers
from reviews.models import reviews

class reviews_serializers(serializers.ModelSerializer):
    class Meta:
        model = reviews
        fields = ('stars', 'body', 'author')
