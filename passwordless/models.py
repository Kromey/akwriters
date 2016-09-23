from django.db import models

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

    @property
    def is_authenticated(self):
        #Anonymous sessions are not authenticated
        return False

    @property
    def is_anonymous(self):
        return True

    def __str__(self):
        return "Anonymous User"

