from django.urls import path
from rest_auth.views import UserDetailsView
from rest_framework.routers import DefaultRouter


from apps.users import views


router = DefaultRouter()
router.register(r'', views.UserDataForStaffViewSet, basename='user')

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('me/events/', views.UserEventsViewSet.as_view({'get': 'list'})),
    path('me/events/<str:event_id>/detailed/', views.UserEventsViewSet.as_view({'get': 'retrieve'})),
]

userpatterns += router.urls

organizationpatterns = [
    path('', views.OrganizationsView.as_view()),
    path('<str:uuid>/', views.DetailsWithAllEventsOrganizationView.as_view()),
    path('<str:uuid>/detailed/', views.DetailedOrganizationView.as_view()),
]
