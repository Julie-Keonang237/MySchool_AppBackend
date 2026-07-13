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
       
        print("🔍 Received data:", request.data) 
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request=request, email=email, password=password)
            
            if user:
                # Check if email is verified
                if not user.is_verified:
                    return Response({
                        "status": "error", 
                        "message": "Please verify your email before logging in. Check your inbox for verification link."
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                if user.check_password(password):
                    token = get_token_for_user(user)
                    return Response({
                    "status": "success",
                    "message": "User Login Successfully",
                    "username": user.email,
                    "tokens": token
                }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error", 
                        "message": "Password has been changed. Please login with the new password"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status": "error", 
                    "message": "Invalid credentials"
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