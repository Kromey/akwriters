from django.conf import settings
from django.contrib.auth.hashers import make_password,is_password_usable
from django.db import models
from django.utils import timezone


from prosody.utils import nodeprep


from . import utils

# Create your models here.

class User(models.Model):
    """
    User model

    This User model eschews passwords, relying instead on emailed OTP tokens.
    """

    username = models.CharField(max_length=30, unique=True)
    jid_node = models.CharField(max_length=30, null=True)
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

    @property
    def jid_domain(self):
        return settings.JABBER_DOMAIN

    @property
    def jid(self):
        return "{node}@{domain}".format(
                node=self.jid_node,
                domain=self.jid_domain,
                )

    def save(self, *args, **kwargs):
        self.jid_node = nodeprep(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class AnonymousUser:
    """
    An object to represent an anonymous/unauthenticated user
    """
    username = ''
    jid_node = ''
    jid_domain = ''
    jid = ''
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
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=80, default=utils.new_app_password)
    created_on = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created_on']

    def save(self, *args, **kwargs):
        if self.password and not is_password_usable(self.password):
            # We have a password that's not already hashed, so let's do that
            # First we normalize it
            password = utils.normalize_app_password(self.password)
            # Then we hash it
            password = make_password(password)

            # Now we put the normalized-and-hashed password where it belongs
            self.password = password

        return super().save(*args, **kwargs)

