from django.urls import path

from authentication.views import ResendVerificationEmailView, SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserLogoutView, UserPasswordResetView, UserProfileView, UserRegistrationView, VerifyEmailView
from .views import *


# Define app_name for namespacing
app_name = 'authentication'

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),  
    # NEW
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'),

]