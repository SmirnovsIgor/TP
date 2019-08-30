from django.urls import path, include


app_name = "api"

urlpatterns = [
    path('events/', include('apps.events.urls', namespace="events")),
]
