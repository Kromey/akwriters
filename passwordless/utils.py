import os
import random
import uuid


from django.contrib.auth.hashers import make_password,is_password_usable
from django.utils import timezone
from datetime import timedelta


WORDLIST_FILE = os.path.join(os.path.dirname(__file__), 'wordlist.txt')


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

    return words

