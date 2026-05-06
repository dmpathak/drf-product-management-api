from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginApiView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("update-user/", UpdateUserView.as_view()),
    path("auth/forgot-password/", ForgotPasswordView.as_view()),
    path("auth/reset-password/", ResetPasswordView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
]
