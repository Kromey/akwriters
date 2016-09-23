from django.db import models

# Create your models here.

class User(models.Model):
    """
    User model

    This User model relies in part on the Prosody model for additional data
    about the user, including password and the XMPP domain.
    """

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=30, null=True)

