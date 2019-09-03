from rest_framework.routers import DefaultRouter
from apps.events import views as event_views

app_name = "api"

router = DefaultRouter()
router.register(r'events', event_views.EventViewSet, basename='event')

urlpatterns = router.urls
