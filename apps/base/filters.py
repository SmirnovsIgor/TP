from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend


class PlaceFilter(filters.FilterSet):
    place = filters.UUIDFilter(field_name="place")


class AddressFilter(filters.FilterSet):
    address = filters.UUIDFilter(field_name="address")


class DateFilter(filters.FilterSet):
    date__gte = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateTimeFilter(field_name="date", lookup_expr="lte")


class SubscriptionDateFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        pass
