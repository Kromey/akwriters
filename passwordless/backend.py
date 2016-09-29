from django.core.exceptions import ObjectDoesNotExist


from . import models


class PasswordlessBackend(object):
    def authenticate(self, token=None):
        try:
            auth = models.AuthToken.objects.get(token=token)

            return auth.user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and user_obj.is_superuser

