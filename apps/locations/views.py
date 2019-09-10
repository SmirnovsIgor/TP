from django.shortcuts import render
from rest_framework import viewsets

from apps.locations.models import Place
from apps.locations.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing Places
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer