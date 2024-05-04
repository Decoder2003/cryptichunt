from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CryptManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_verified', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be assigned to is_superuser=True')
        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('Email id is necessary'))
        email = self.normalize_email(email)
        user= self.model(email=email, user_name=user_name,first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()   

        return user

class cryptUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    discord_id = models.CharField(max_length=50, unique=True)
    college_name = models.CharField(max_length=50)
    college_roll_number = models.CharField(max_length=100, null=True)
    answers = models.TextField(default="{}")
    score = models.IntegerField(default=0)
    current_level = models.IntegerField(default=0)
    date_time = models.TextField(default='{}')
    rank = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=datetime.now)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CryptManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS  = ['email','first_name','discord_id']
    
    def __str__(self):
        return self.user_name

class quesAns(models.Model):
    question_number = models.IntegerField(default=0)
    answer = models.TextField(null=True)

    def __str__(self):
        return f"{self.question_number}"

class alerts(models.Model):
    Type = models.CharField(max_length=150)
    Content = models.CharField(max_length=350)
    Time = models.DateTimeField(default=datetime.now)
