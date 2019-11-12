import os
import random
import re
from urllib.parse import urlparse
import uuid


from django.shortcuts import redirect
from django.urls import resolve
from django.utils import timezone
from datetime import timedelta


WORDLIST_FILE = os.path.join(os.path.dirname(__file__), 'wordlist.txt')


class InvalidRedirect(Exception):
    pass

def _validate_redirect(path):
    try:
        p = urlparse(path).path
        _ = resolve(p)

        return p
    except:
        raise InvalidRedirect(path)

def safe_redirect(path, default='/'):
    try:
        return redirect(_validate_redirect(path))
    except InvalidRedirect:
        return redirect(default)


def make_token():
    """
    Generate a random token suitable for activation/confirmation via email

    A hex-encoded random UUID has plenty of entropy to be secure enough for our
    needs.
    """
    return uuid.uuid4().hex


def expiration_date():
    """
    AuthToken objects expire 1 hour after creation by default
    """
    return timezone.now() + timedelta(hours=1)


def new_app_password(size=6):
    f = open(WORDLIST_FILE, 'r')

    words = []
    for i in range(size):
        words.append(next(f).strip())

    for num,line in enumerate(f):
        j = random.randrange(size+num)
        if j < size:
            words[j] = line.strip()

    return ' '.join(words)


_re = re.compile(r'[^a-z]')
def normalize_app_password(password):
    """
    Normalize the App Password

    Do this before hashing, saving, or validating an app password; in this case,
    normalization means lower-casing the string and removing any non-alphabetic
    characters.
    """
    return _re.sub('', password.lower())

