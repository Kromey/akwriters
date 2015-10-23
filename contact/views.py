import binascii


from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail


from contact.forms import ContactForm

# Create your views here.

def contact(request):
    form_init = {
            'username': request.user.username,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'email': request.user.email,
            }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Success!')
        else:
            messages.error(request, 'Boo! Hiss!')
    else:
        form = ContactForm(initial=form_init)

    return render(request, 'contact/contact.html', {'form': form})

