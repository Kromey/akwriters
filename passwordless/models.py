from django.db import models
from django.utils import timezone


from . import utils

# Create your models here.

class User(models.Model):
    """
    User model

    This User model eschews passwords, relying instead on emailed OTP tokens.
    """

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)

    @property
    def is_authenticated(self):
        #Used to tell authenticated Users from anonymous ones
        return True

    @property
    def is_anonymous(self):
        #This is not an anonymous user
        return False

    def __str__(self):
        return self.username


class AnonymousUser:
    """
    An object to represent an anonymous/unauthenticated user
    """
    username = ''
    email = None
    is_active = False
    is_superuser = False
    date_joined = None
    last_login = None

    @property
    def is_authenticated(self):
        #Anonymous sessions are not authenticated
        return False

    @property
    def is_anonymous(self):
        return True

    def __str__(self):
        return "Anonymous User"


class AuthToken(models.Model):
    """
    OTP Token for passwordless authentication
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, default=utils.make_token, unique=True)
    session_key = models.CharField(max_length=40, default=utils.make_token)
    date_sent = models.DateTimeField(default=timezone.now)
    date_expires = models.DateTimeField(default=utils.expiration_date)

    @property
    def is_valid(self):
        return self.date_expires >= timezone.now()


class AppPassword(models.Model):
    """
    Generated application passwords
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=80)
    created_on = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(null=True)

