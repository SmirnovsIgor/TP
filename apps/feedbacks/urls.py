from rest_framework.routers import DefaultRouter

from apps.feedbacks import views


router = DefaultRouter()
router.register('', views.CommentViewSet, basename='comments')

commentpatterns = router.urls
