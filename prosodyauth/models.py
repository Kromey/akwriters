from datetime import datetime, timedelta
import uuid


from django.db import models, connection


from prosodyauth.prosody import db


# Create your models here.

class User(models.Model):
    """
    User model

    This user model is designed around the concept of XMPP JIDs, and is
    therefore intended to represent users as 'username'@'domain'. For this
    reason it allows duplicate usernames, provided each has a distinct domain
    part.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._lastlog_data = db.get_data_store(self.username, self.domain, 'lastlog')
        except:
            self._lastlog_data = {}

    username = models.CharField(max_length=30, unique=True)
    domain = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=30, null=True)

    _lastlog_data = None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    @property
    def xmpp_online(self):
        if self._lastlog_data.get('event') == 'login':
            return True
        else:
            return False

    @property
    def xmpp_last_login(self):
        return datetime.utcfromtimestamp(self._lastlog_data.get('timestamp'))

    @property
    def xmpp_last_ip(self):
        return self._lastlog_data.get('ip')

    @property
    def last_login(self):
        try:
            last_login = LoginAudit.objects.latest('login_date')
            return last_login.login_date
        except LoginAudit.DoesNotExist:
            return None

    @last_login.setter
    def last_login(self, value):
        last_login = LoginAudit(user=self, login_date=value, ip='0.0.0.0')
        last_login.save()

    def is_authenticated(self):
        #Used to tell authenticated Users from anonymous ones
        return True

    def is_anonymous(self):
        #This is not an anonymous user
        return False

    def __str__(self):
        return self.username


def make_token():
    return uuid.uuid4().hex

class ConfirmationBase(models.Model):
    """
    Abstract class for models that depend upon email confirmation.
    """
    user = models.OneToOneField(User, primary_key=True)
    token = models.CharField(max_length=40, default=make_token)
    date_sent = models.DateTimeField(auto_now=True)

    _expiration_hours = 24

    @property
    def expiration_date(self):
        return self.date_sent + timedelta(hours=self._expiration_hours)

    class Meta:
        abstract = True

class EmailConfirmation(ConfirmationBase):
    """
    Track pending email confirmations

    When a user changes their email address, the new address is put into an
    EmailConfirmation object until the user confirms it; while in this object,
    the new address is considered unconfirmed and not in use.
    """
    email = models.EmailField()

    def __str__(self):
        return 'Unconfirmed: {}'.format(self.email)

class RegistrationConfirmation(ConfirmationBase):
    """
    Track pending user registrations
    """
    password = models.CharField(max_length=40)
    iterations = models.IntegerField(default=8192)

    def __str__(self):
        return 'Unconfirmed: {}'.format(self.user.username)


class LoginAudit(models.Model):
    """
    Track user login events

    Using this model allows the site to report previous logins to the user,
    allowing them to potentially spot security breaches of their account.
    """
    user = models.ForeignKey(User)
    login_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

class AnonymousUser:
    """
    An object to represent an anonymous/unauthenticated user
    """
    username = ''
    domain = ''
    email = None
    first_name = None
    last_name = None
    is_active = False
    is_superuser = False
    date_joined = None
    timezone = None

    # These are the @properties from the User object
    full_name = "Anonymous User"
    xmpp_online = False
    xmpp_last_login = None
    xmpp_last_ip = None
    last_login = None

    def is_authenticated(self):
        #Anonymous sessions are not authenticated
        return False

    def is_anonymous(self):
        return True

    def __str__(self):
        return "Anonymous User"
