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

class ProsodyAccountsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(store='accounts')

class ProsodyRosterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(store='roster')

