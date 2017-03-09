from rest_framework import viewsets
from reviews_rest.reviews_serializers import reviews_serializers
from reviews.models import reviews

class reviews_viewsets(viewsets.ModelViewSet):
    queryset = reviews.objects.all()
    serializer_class = reviews_serializers

