from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, user_name, user_surname, telephone, role, password=None, passwordConfirm=None, **extra_fields):
        """
        Create and return a regular user
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        if not user_name:
            raise ValueError("Users must have a username")
        
        # Check password confirmation
        if password and passwordConfirm and password != passwordConfirm:
            raise ValueError("Passwords don't match")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            user_name=user_name,
            user_surname=user_surname,
            telephone=telephone,
            role=role,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, user_surname, telephone, role, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email=email,
            user_name=user_name,
            user_surname=user_surname,
            telephone=telephone,
            role=role,
            password=password,
            passwordConfirm=password,
            **extra_fields
        )


class User(AbstractUser):
    """
    Custom User Model
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),  # Fixed: 'otheruser' instead of 'otheruser'
    ]
 
    username = None

    # Required fields
    email = models.EmailField(verbose_name="email", max_length=300, unique=True)
    user_name = models.CharField(max_length=200)
    user_surname = models.CharField(max_length=200)
    telephone = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    sexe = models.CharField(max_length=100, blank=True, null=True)
    
    # Custom fields
    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)     # ✅ must be a field
    is_superuser = models.BooleanField(default=False) #

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "user_name",
        "user_surname",
        "telephone",
        "role"
    ]


    # Set custom manager
    objects = UserManager()


    class Meta:
        db_table = 'users'  # Optional: specify table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.user_name} {self.user_surname}"

    def get_short_name(self):
        return self.user_name

   