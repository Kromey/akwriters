from datetime import datetime, timedelta
from decimal import Decimal
import json
import uuid


from django.conf import settings
from django.db import models, connection
from django.utils import timezone


from prosodyauth import authenticate, managers
from prosodyauth.prosody.parsejid import nodeprep


# Create your models here.

def getProsodyDomain():
    return settings.PROSODY_DEFAULT_DOMAIN

class Prosody(models.Model):
    """
    Prosody model

    This model provides an interface for Django to access Prosody's database
    table. Each item in this table is indexed by Prosody via the tuple of
    (host,user,store,key). The type field describes the type of data that is
    stored in the value field, and can be one of:
      * string: String data
      * number: A (potentially) floating-point number
      * json: A JSON string
      * boolean: Simple true/false
    Note that this app assumes that Prosody is configured not to manage its own
    table; letting Prosody manage its table will very probably make it unusable
    in Django, and/or result in data loss.
    """

    host = models.TextField(default=getProsodyDomain)
    user = models.TextField(db_index=True)
    store = models.TextField(db_index=True)
    key = models.TextField(db_index=True)
    type = models.TextField(default='string')
    value = models.TextField()

    # Custom managers
    objects = managers.ProsodyQuerySet.as_manager()
    accounts = managers.ProsodyAccountsManager.from_queryset(managers.ProsodyQuerySet)()
    roster = managers.ProsodyRosterManager.from_queryset(managers.ProsodyQuerySet)()

    @property
    def decoded(self):
        if not self.type:
            raise AttributeError('Cannot decode value without a type')
        elif self.type == 'string':
            return self.value
        elif self.type == 'number':
            return Decimal(self.value)
        elif self.type == 'json':
            return json.loads(self.value)
        elif self.type == 'boolean':
            return self.value == "true"
        else:
            raise AttributeError('Unknown type definition: {}'.format(self.type))

    def encode(self, value):
        """Encode a native Python object into a string for Prosody's database.

        This method uses the type field to assume the type of the object being
        supplied, or more accurately to choose the correct method for encoding
        the supplied value into a string for Prosody.

        WARNING: This method REQUIRES that the store and key properties are
        already set correctly in order for it to properly detect the type.

        SIDE EFFECTS: This method may change the value of the type property, in
        the same manner as the save() method maps it based on store and key.
        """
        self._set_type()

        if self.type == 'boolean':
            if value:
                self.value = "true"
            else:
                self.value = "false"
        elif self.type == 'json':
            # Use a compact JSON encoding
            self.value = json.dumps(value, separators=(',', ':'))
        elif self.type == 'number' or self.type == 'string':
            self.value = str(value)
        else:
            raise AttributeError('Unknown type definition: {}'.format(self.type))

    def save(self, *args, **kwargs):
        #We need to set type correctly for Prosody to understand it
        self._set_type()

        #We also do some additional processing of username here
        self.user = nodeprep(self.user)

        super().save(*args, **kwargs)

    def _set_type(self):
        """Set the type field to ensure Prosody can understand the value.

        Prosody relies on the type field in order to understand how to process
        the value. To help ensure that whatever we do to Prosody's database is
        usable by Prosody, we map some known store and store/key values to the
        proper type value that Prosody expects to find there.

        However, we do not guarantee that the mapping in here is exhaustive, so
        we allow the type to be overridden (or simply fall back to the default)
        in cases where we don't explicitly map type.
        """
        if self.store == 'lastlog' and self.key == 'timestamp':
            self.type = 'number'
        elif self.store == 'lastlog':
            self.type = 'string'
        elif self.store == 'accounts' and self.key == 'iteration_count':
            self.type = 'number'
        elif self.store == 'accounts':
            self.type = 'string'
        elif self.store == 'roster':
            self.type = 'json'
        elif self.key == 'persistence':
            self.type = 'boolean'

    class Meta:
        #Prosody is hard-coded to use the prosody table, so that's what we use
        db_table = 'prosody'
        #Uniqueness is based on user,store,key (and host, but we're single-host)
        unique_together = (("user","store","key"),)

    def __str__(self):
        return "{}.{}.{}".format(self.user, self.store, self.key)

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

    _lastlog_data = None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    @property
    def xmpp_online(self):
        if self._get_lastlog('event') == 'login':
            return True
        else:
            return False

    @property
    def xmpp_last_login(self):
        #TODO: Name is misleading, as the result could also be the last logoff
        #TODO: There seems to be significant timezone-related issues here
        return datetime.utcfromtimestamp(self._get_lastlog('timestamp'))

    @property
    def xmpp_last_ip(self):
        return self._get_lastlog('ip')

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

    def set_password(self, password=None, salt=None, salted_pass=None, iterations=settings.SCRAM_ITERATIONS):
        if salted_pass is None:
            if salt is None:
                #No salt provided, make some
                salt = authenticate.make_salt()

            #Salt the password
            salted_pass = authenticate.salt_password(password, salt, iterations)

        #Generate our keys
        #I believe the standard only requires us to store one of these, but
        # Prosody stores both and I don't know why -- so we will too.
        stored_key, server_key = authenticate.compute_keys(salted_pass)

        #And now we get to stash all of our values into Prosody's table
        Prosody.accounts.update_or_create(user=self.username, key='iteration_count', defaults={'value': iterations})
        Prosody.accounts.update_or_create(user=self.username, key='salt', defaults={'value': salt})
        Prosody.accounts.update_or_create(user=self.username, key='stored_key', defaults={'value': stored_key})
        Prosody.accounts.update_or_create(user=self.username, key='server_key', defaults={'value': server_key})

    def __str__(self):
        return self.username

    def _get_lastlog(self, key):
        """
        Get data from Prosody's lastlog store

        Prosody stores information about the last logon/logoff in the rows with
        store='lastlog'. We grab them here and index them so that we can display
        this data to/about users. The entire store is cached within the User
        instance so that we don't generate too much database churn.
        """

        if self._lastlog_data is None:
            #No lastlog data fetched yet, go fetch it
            store = Prosody.objects.filter(user__iexact=self.username, store='lastlog')
            self._lastlog_data = dict()
            for item in store:
                #Process into a dict for easy referencing
                if item.type == 'number':
                    #Safer to do a floating-point conversion, but we know that
                    #lastlog only has integers (well, one integer...)
                    self._lastlog_data[item.key] = int(item.value)
                else:
                    self._lastlog_data[item.key] = item.value

        return self._lastlog_data.get(key)


def make_token():
    """
    Generate a random token suitable for activation/confirmation via email

    A hex-encoded random UUID has plenty of entropy to be secure enough for our
    needs.
    """
    return uuid.uuid4().hex

class ConfirmationBase(models.Model):
    """
    Abstract class for models that depend upon email confirmation.
    """
    user = models.OneToOneField(User, primary_key=True)
    token = models.CharField(max_length=40, default=make_token)
    date_sent = models.DateTimeField(default=timezone.now)

    _expiration_hours = 24

    @property
    def expiration_date(self):
        return self.date_sent + timedelta(hours=self._expiration_hours)

    @property
    def is_valid(self):
        return self.expiration_date >= timezone.now()

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
