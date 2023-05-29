from django.urls import path
from .views import register_user, user_login, otp_verify

urlpatterns = [
    path('register', register_user, name='register_user'),
    path('login', user_login, name='user_login'),
    path('otp_verify',otp_verify, name='otp_verify'),
]
