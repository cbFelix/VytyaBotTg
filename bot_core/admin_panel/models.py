from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class TgUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    language_code = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UserMessage(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    message_text = models.TextField()
    date_received = models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField()

    def __str__(self):
        return self.question_text


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser):
    ACCESS_LEVEL_CHOICES = [
        (1, 'Unauthenticated'),
        (2, 'User'),
        (3, 'Moderator'),
        (4, 'Admin'),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    access_level = models.PositiveSmallIntegerField(choices=ACCESS_LEVEL_CHOICES, default=1)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'access_level', 'is_active', 'is_staff')
    list_filter = ('access_level', 'is_active', 'is_staff')
    search_fields = ('email', 'name')


admin.site.register(User, UserAdmin)


