from django.urls import path


from apps.users.views import PersonalData

urlpatterns = [
    path('user/personal-data/', PersonalData.as_view()),
]
