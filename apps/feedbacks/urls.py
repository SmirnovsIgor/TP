from rest_framework.routers import DefaultRouter

from apps.feedbacks import views


router = DefaultRouter()

router.register(r'', views.ReviewViewSet, basename='review')
router.register(r'', views.CommentViewSet, basename='comments')

reviewpatterns = router.urls
commentpatterns = router.urls
