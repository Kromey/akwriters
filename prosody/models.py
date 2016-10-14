from decimal import Decimal
import json


from django.db import models


from . import managers
from . import utils

# Create your models here.
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

    host = models.TextField(default=utils.getProsodyDomain)
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
        self.user = utils.nodeprep(self.user)

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
        ordering = ['user','store','key',]
        #Prosody is hard-coded to use the prosody table, so that's what we use
        db_table = 'prosody'
        #Uniqueness is based on user,store,key (and host, but we're single-host)
        unique_together = (("user","store","key"),)

    def __str__(self):
        return "/{}/{}/{}".format(self.user, self.store, self.key)


class ProsodyRoster(Prosody):
    objects = managers.ProsodyRosterManager.from_queryset(managers.ProsodyQuerySet)()

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = 'roster'

    def save(self, *args, **kwargs):
        self.store = 'roster'
        super().save(*args, **kwargs)

