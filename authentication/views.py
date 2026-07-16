from django.shortcuts import render

# Create your views here.
from django.db.migrations import serializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import *
from . utils import *
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.utils.html import escape

import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import User



def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }




from email_validator import validate_email as validate_real_email, EmailNotValidError
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")

        if not email:
            return Response(
                {
                    "status": "error",
                    "message": "Email is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate syntax and deliverability
        try:
            validated = validate_real_email(
                email,
                check_deliverability=True
            )

            email = validated.email

        except EmailNotValidError as e:

            return Response(
                {
                    "status": "error",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():

            return Response(
                {
                    "status": "error",
                    "message": "A user with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["email"] = email

        serializer = UserRegistrationSerializer(data=data)

        if not serializer.is_valid():

            return Response(
                {
                    "status": "error",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        user.is_verified = False
        user.is_active = False
        user.save()

        success, message = send_verification_email(user)

        if not success:

            user.delete()

            return Response(
                {
                    "status": "error",
                    "message": message
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "status": "success",
                "message":
                    "Registration successful. Please check your email to verify your account."
            },
            status=status.HTTP_201_CREATED,
        )

class VerifyEmailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        uid = request.GET.get("uid")
        token = request.GET.get("token")

        if not uid or not token:

            return Response(
                {
                    "status": "error",
                    "message": "Invalid verification link."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            user_id = urlsafe_base64_decode(uid).decode()

            user = User.objects.get(id=user_id)

        except Exception:

            return Response(
                {
                    "status": "error",
                    "message": "Invalid verification link."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if PasswordResetTokenGenerator().check_token(user, token):

            user.is_verified = True
            user.is_active = True

            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Email verified successfully."
                }
            )

        return Response(
            {
                "status": "error",
                "message": "Verification link has expired."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class VerifyEmailRedirectView(APIView):
    """
    Landing page used as the link inside the verification email.

    Most email clients (Gmail included) only auto-linkify http(s) URLs, not
    custom schemes like "myschool://" — so the email link itself must be a
    normal http(s) URL. On a phone with the app installed, this page hands
    off to the Flutter app's deep link (myschool://verify-email?...).

    But a human can also open this link with no app installed to catch the
    deep link at all — e.g. during dev, testing against Flutter web on a
    desktop browser, or on a machine that just doesn't have the app. There's
    no way to know in advance which case applies, and the backend can't
    guess the Flutter web dev server's port to redirect there either. So
    this view verifies the email itself (same check as VerifyEmailView)
    before rendering anything: verification always succeeds from this page
    alone, and the deep-link handoff underneath is just a bonus for mobile.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        raw_uidb64 = request.GET.get('uidb64', '')
        raw_token = request.GET.get('token', '')
        uidb64 = escape(raw_uidb64)
        token = escape(raw_token)
        deep_link = f"myschool://verify-email?uidb64={uidb64}&token={token}"

        serializer = VerifyEmailSerializer(data={'uidb64': raw_uidb64, 'token': raw_token})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_verified = True
            user.save()
            heading = "Email verifie !"
            message = "Votre email a ete verifie avec succes. Vous pouvez desormais vous connecter."
        else:
            # validate() raises ValidationError({"status": ..., "message": ...});
            # DRF turns each dict key into a field with a list of ErrorDetail,
            # so the message is errors['message'][0], not errors['message'].
            errors = serializer.errors
            message_errors = errors.get('message') or []
            already_verified = bool(message_errors) and str(message_errors[0]) == 'Email already verified'
            if already_verified:
                heading = "Email deja verifie"
                message = "Cet email a deja ete verifie. Vous pouvez vous connecter."
            else:
                heading = "Lien invalide"
                message = "Ce lien de verification est invalide ou a expire. Demandez-en un nouveau depuis l'application."

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Verification de l'email</title>
  <meta http-equiv="refresh" content="0; url={deep_link}">
</head>
<body style="font-family: sans-serif; text-align: center; padding-top: 60px;">
  <h2>{heading}</h2>
  <p>{message}</p>
  <p>Ouverture de l'application My School...</p>
  <p>Si rien ne se passe (par exemple depuis un ordinateur), <a href="{deep_link}">appuyez ici</a> pour ouvrir l'application, ou fermez cet onglet et connectez-vous directement.</p>
</body>
</html>"""
        return HttpResponse(html)


class VerifyEmailOTPView(APIView):
    """
    Verify email using the 6-digit code sent alongside the link.
    Expects: {"email": "user@example.com", "otp": "123456"}
    """
    serializer_class = VerifyEmailOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            user.is_verified = True
            user.verification_otp = None
            user.verification_otp_expires_at = None
            user.save()

            token = get_token_for_user(user)

            return Response({
                "status": "success",
                "message": "Email verified successfully",
                "email": user.email,
                "user_name": user.user_name,
                "token": token
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    """
    Resend verification email
    Expects: {"email": "user@example.com"}
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            
            # Resend verification email
            success, message = send_verification_email(user, request)
            
            if success:
                return Response({
                    "status": "success", 
                    "message": "Verification email resent successfully. Please check your inbox."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error", 
                    "message": f"Failed to send email: {message}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = authenticate(request=request, email=email, password=password)
            
            if user is not None:
                # Check if email is verified
                if not user.is_verified:
                    return Response({
                        "status": "error",
                        "message": "Please verify your email before logging in. Check your inbox for the verification link."
                    }, status=status.HTTP_403_FORBIDDEN)  # 403 more appropriate than 401
                
                # Optional: Check if user is active
                if not user.is_active:
                    return Response({
                        "status": "error",
                        "message": "Your account has been deactivated. Please contact support."
                    }, status=status.HTTP_403_FORBIDDEN)
                
                token = get_token_for_user(user)
                return Response({
                    "status": "success",
                    "message": "User logged in successfully",
                    "user": {
                        "email": user.email,
                        # Add any other user fields you want to return
                    },
                    "tokens": token
                }, status=status.HTTP_200_OK)
            
            # Authentication failed
            return Response({
                "status": "error",
                "message": "Invalid email or password. Please try again."
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserChangePasswordView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            update_session_auth_hash(request, request.user)
            return Response({
                "status": "success", 
                "message": "Password Changed Successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error", 
            "message": "Password reset failed. Please try again later."
        }, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    serializer_class = SendPasswordResetEmailSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                "status": "success", 
                "message": "Password reset email has been sent successfully. Please check your email inbox or spam folder."
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error", 
            "message": "Password reset failed. Please try again later."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, uid, token, *args, **kwargs):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({
                "status": "success", 
                "message": "Password Changed Successfully"
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error", 
            "message": "Password reset link has expired. Please request a new link or Invalid Link"
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                "status": "success", 
                "message": "User Logout Successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RefreshAccessTokenView(APIView):
    permission_classes = []

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)

            return Response({
                "access": str(refresh.access_token)
            })

        except TokenError:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )