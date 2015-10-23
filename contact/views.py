import binascii


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404


from contact.forms import ContactForm

# Create your views here.

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success('Success!')
        else:
            messages.error('Boo! Hiss!')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

