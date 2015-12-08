from django.db import models


from prosodyauth.prosody import parsejid


# Custom model managers/querysets

class ProsodyQuerySet(models.QuerySet):
    def filter(self, **kwargs):
        try:
            user = parsejid.nodeprep(kwargs['user'])
            kwargs['user'] = user
        except KeyError:
            # No user in our kwargs
            pass

        return super().filter(**kwargs)

    def get(self, **kwargs):
        try:
            user = parsejid.nodeprep(kwargs['user'])
            kwargs['user'] = user
        except KeyError:
            # No user in our kwargs
            pass

        return super().get(**kwargs)

class ProsodyStoreBase(models.Manager):
    """Base class for Managers intended to access a Prosody store

    By overriding self.prosody_store, child classes of this one can easily
    implement custom access to a Prosody data store without having to fuss with
    any of the particulars.
    """
    prosody_store = None

    def get_queryset(self):
        return super().get_queryset().filter(store=self.prosody_store)

    def update_or_create(self, *args, **kwargs):
        return super().update_or_create(store=self.prosody_store, *args, **kwargs)

class ProsodyAccountsManager(ProsodyStoreBase):
    """Custom Manager to access the Prosody 'accounts' data store"""
    prosody_store = 'accounts'

class ProsodyRosterManager(models.Manager):
    """Custom Manager to access the Prosody 'roster' data store"""
    prosody_store = 'roster'

