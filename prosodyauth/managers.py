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

