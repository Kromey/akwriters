import binascii
from passlib.hash import scram
import hmac
from hashlib import sha1
import uuid
import string
import re


from django.conf import settings


def password_is_compliant(password, username):
    """
    Check whether or not this password complies with the site's password policy

    Specifically, the password must:
     * Be at least 8 characters long
     * Have at least two of: Upper-case letters, lower-case letters, numbers, punctuation
     * Not include the user's username
    """

    #Check length
    if len(password) < 8:
        return False

    #Check for complexity
    score = 0
    #Upper-case letters
    if password_contains(password, string.ascii_uppercase):
        score = score + 1
    #Lower-case letters
    if password_contains(password, string.ascii_lowercase):
        score = score + 1
    #Numbers
    if password_contains(password, string.digits):
        score = score + 1
    #Punctuation
    if password_contains(password, string.punctuation):
        score = score + 1

    if score < 2:
        return False

    #Password must not contain username
    if username.lower() in password.lower():
        return False

    #If we've gotten here, we've passed all the tests
    return True


def password_contains(password, contents):
    pattern = "[{}]".format(contents)

    if re.search(pattern, password) is None:
        return False
    else:
        return True


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
