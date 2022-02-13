from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import TeacherRegistration, LogoutAPIView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutAPIView.as_view()),
    path('register/teacher/', TeacherRegistration.as_view()),
]
