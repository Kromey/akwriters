import binascii
from passlib.hash import scram
import hmac
from hashlib import sha1
import uuid


from django.conf import settings


def verify_password(password, salt, iterations, stored_key, server_key):
    salted_pass = salt_password(password, salt, iterations)

    return stored_key == compute_stored_key(salted_pass) and server_key == compute_server_key(salted_pass)


def make_salt():
    """
    Generate a random salt

    A hex-encoded random UUID has plenty of entropy to be secure enough for our
    needs.
    """
    return uuid.uuid4().hex


def salt_password(password, salt, iterations=settings.SCRAM_ITERATIONS):
    if salt is None:
        salt = make_salt()

    raw = scram.derive_digest(password, salt.encode('utf-8'), int(iterations), 'sha-1')
    return binascii.hexlify(raw)


def compute_keys(salted_pass):
    return compute_stored_key(salted_pass), compute_server_key(salted_pass)


def compute_stored_key(salted_pass):
    key = binascii.unhexlify(salted_pass)
    h = sha1()
    h.update(hmac.new(key, b'Client Key', sha1).digest())
    return h.hexdigest()


def compute_server_key(salted_pass):
    key = binascii.unhexlify(salted_pass)
    return hmac.new(key, b'Server Key', sha1).hexdigest()
