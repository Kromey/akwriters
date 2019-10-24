from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


from contact.forms import ContactForm

# Create your views here.

@login_required
def contact(request):
    try:
        username = request.user.username
        email = request.user.email
    except AttributeError:
        username = ''
        email = None

    form_init = {
            'username': username,
            # 'ip_address': request.META.get('REMOTE_ADDR'),
            'email': email,
            }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = render_to_string('contact/email.txt', form.cleaned_data)
            send_mail('Contact Us email form', msg, settings.EMAIL_SENDER, [settings.CONTACT_EMAIL])

            messages.success(request, 'Thank you for contacting us!')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Boo! Hiss!')
    else:
        form = ContactForm(initial=form_init)

    return render(request, 'contact/contact.html', {'form': form})

