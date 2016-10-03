from datetime import timedelta
import uuid


from django.db import models
from django.utils import timezone

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


def make_token():
    """
    Generate a random token suitable for activation/confirmation via email

    A hex-encoded random UUID has plenty of entropy to be secure enough for our
    needs.
    """
    return uuid.uuid4().hex


def expiration_date():
    """
    AuthToken objects expire 1 hour after creation by default
    """
    return timezone.now() + timedelta(hours=1)

class AuthToken(models.Model):
    """
    OTP Token for passwordless authentication
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, default=make_token, unique=True)
    session_key = models.CharField(max_length=40, default=make_token)
    date_sent = models.DateTimeField(default=timezone.now)
    date_expires = models.DateTimeField(default=expiration_date)

    @property
    def is_valid(self):
        return self.date_expires >= timezone.now()

