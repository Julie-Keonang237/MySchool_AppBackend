# authentication/serializers.py
from tokenize import TokenError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from authentication.utils import Util
from authentication.models import *
from django.contrib.auth import authenticate
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone  # ADD THIS

from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'user_surname', 'telephone', 'password', 
                  'passwordConfirm', 'role', 'is_verified', 'is_active', 
                  'is_admin', 'is_online', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        passwordConfirm = attrs.get('passwordConfirm')
        
        if password != passwordConfirm:
            raise serializers.ValidationError({"status": "error", "Message": "Password and Confirm Password Doesn't Match"})
        
        # Remove tc validation
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# This is the important change - REPLACE your VerifyEmailSerializer
class VerifyEmailSerializer(serializers.Serializer):
    """Verify email using token - NO OTP"""
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        User = get_user_model()
        
        try:
            # Decode the user ID
            uid = smart_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(id=uid)
            
            # Check token using Django's built-in PasswordResetTokenGenerator
            if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
                raise serializers.ValidationError({
                    "status": "error", 
                    "message": "Invalid or expired verification link"
                })
            
            if user.is_verified:
                raise serializers.ValidationError({
                    "status": "error", 
                    "message": "Email already verified"
                })
            
            attrs['user'] = user
            return attrs
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({
                "status": "error", 
                "message": "Invalid verification link"
            })


# ADD THIS NEW serializer
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
       
        User = get_user_model()
        
        try:
            user = User.objects.get(email=attrs['email'])
            if user.is_verified:
                raise serializers.ValidationError({
                    "status": "error", 
                    "message": "Email already verified"
                })
            attrs['user'] = user
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "status": "error", 
                "message": "No user found with this email"
            })

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['id', 'email']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError({"status": "error", "message": "Email or password doesn't match. Please try again."})

        if not user.is_verified:
            raise serializers.ValidationError({"status": "error", "message": "Account not verified. Please check your email for verification link."})
        
        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['id', 'user', 'user_name']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    passwordConfirm = serializers.CharField(max_length=255, style={'input_type': 'passwordConfirm'}, write_only=True)

    class Meta:
        fields = ['old_password', 'new_password', 'passwordConfirm']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        passwordConfirm = attrs.get('passwordConfirm')
        user = self.context.get('user')
        if not check_password(old_password, user.password):
            raise serializers.ValidationError({"status": "error", "message": "Old Password is Incorrect."})

        if password == old_password:
            raise serializers.ValidationError({"status": "error", "message": "New Password must be different from the Old Password."})

        if password != passwordConfirm:
            raise serializers.ValidationError({"status": "error", "message": "New Password and Confirm Password don't match."})
        return attrs

    def save(self, **kwargs):
        user = self.context.get('user')
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/api/user/reset-password/' + uid + '/' + token + '/'
            body = 'Your password reset link is ' + link
            data = {
                'subject': 'Password reset',
                'body': body,
                'to_email': user.email,  # FIXED: was 'user' not 'user.email'
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError({"status": "error", "message": "Email not found."})


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    passwordConfirm = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'passwordConfirm']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            passwordConfirm = attrs.get('passwordConfirm')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != passwordConfirm:
                raise serializers.ValidationError({"status": "error", "message": "Password and Confirm Password don't match."})
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"status": "error", "message": "Invalid token."})
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError({"status": "error", "message": "Invalid token."})


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({"status": "error", "message": "Invalid token."})