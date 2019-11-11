from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


from . import models
from . import utils


class PasswordlessBackendBase(object):
    def get_user(self, user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and user_obj.is_superuser


class TokenBackend(PasswordlessBackendBase):
    def authenticate(self, request, token, session_key=None, username=None):
        if session_key is None and username is None:
            # Django's authentication framework uses inspection before actually
            # calling us, so we can't "fake" a TypeError here; best we can do
            # is just return None, i.e. not authenticate the user
            return None

        # Clear out any expired tokens
        models.AuthToken.clear_expired_tokens()

        try:
            auth = models.AuthToken.objects.get(token=token)
            user = auth.user
            valid = auth.is_valid

            if session_key is not None:
                valid = valid and auth.session_key == session_key
            else:
                valid = valid and user.username.lower() == username.lower()

            auth.delete()

            if valid:
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None


class AppPasswordBackend(PasswordlessBackendBase):
    def authenticate(self, request, username, password):
        try:
            password = utils.normalize_app_password(password)

            for ap in models.AppPassword.objects.filter(user__username__iexact=username):
                if check_password(password, ap.password):
                    # This is the one, record last_used
                    ap.last_used = timezone.now()
                    ap.save()
                    return ap.user

            return None
        except ObjectDoesNotExist:
            return None

