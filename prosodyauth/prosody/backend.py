from passlib.hash import scram
import hmac
from hashlib import sha1


from django.conf import settings


from prosodyauth.models import User
from prosodyauth.prosody.datastore import ProsodyDatastore


class ProsodyBackend:
    """
    Authenticate against the Prosody XMPP server's database storage.

    Use the username, domain, and (plain) password.
    """


    def authenticate(self, username=None, domain=None, password=None):
        if domain is None:
            domain = settings.PROSODY_DEFAULT_DOMAIN

        login_valid = self._check_password(username=username, domain=domain, password=password)
        if login_valid:
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                # Create a new user. Note that we don't set password, because
                # Prosody will manage it.
                user = User(username=username, domain=domain, is_active=True)
                user.save()
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def _check_password(self, username, domain, password):
        data = ProsodyDatastore.get_data_store(username, domain, 'accounts')

        try:
            salted_pass = self._salt_password(password, data['salt'], data['iteration_count'])
            stored_key = self._stored_key(salted_pass)
            server_key = self._server_key(salted_pass)

            return (stored_key == data['stored_key'] and server_key == data['server_key'])
        except KeyError:
            return False


    def _salt_password(self, password, salt, iterations):
        return scram.derive_digest(password, salt.encode('utf-8'), int(iterations), 'sha-1')


    def _stored_key(self, salted_pass):
        h = sha1()
        h.update(hmac.new(salted_pass, b'Client Key', sha1).digest())
        return h.hexdigest()


    def _server_key(self, salted_pass):
        return hmac.new(salted_pass, b'Server Key', sha1).hexdigest()
