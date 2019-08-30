from django.urls import path
from apps.events import views


app_name = "events"

urlpatterns = [
    path('', views.EventList.as_view(), name='events_list'),
    path('<uuid:id>/', views.EventDetail.as_view(), name='events_detail'),
]
