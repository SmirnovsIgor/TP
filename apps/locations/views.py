from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from apps.locations.models import Place
from apps.locations.serializers import PlaceSerializer


class PlaceViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    A ViewSet for listing and retrieving Places
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
