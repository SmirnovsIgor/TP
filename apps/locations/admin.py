from django.contrib import admin

from apps.locations.models import Place, Address


admin.site.register(Place)
admin.site.register(Address)
