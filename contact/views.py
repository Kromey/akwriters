from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


from contact.forms import ContactForm

# Create your views here.

def contact(request):
    form_init = {
            'username': request.user.username,
            # 'ip_address': request.META.get('REMOTE_ADDR'),
            'email': request.user.email,
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

