import os
import random


from django.contrib.auth.hashers import make_password,is_password_usable


WORDLIST_FILE = os.path.join(os.path.dirname(__file__), 'wordlist.txt')


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

