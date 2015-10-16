import binascii


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404


from prosodyauth.forms import LoginForm, RegistrationForm
from prosodyauth.prosody.backend import ProsodyBackend
from prosodyauth import utils
from prosodyauth.models import User, RegistrationConfirmation


backend = ProsodyBackend()

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = backend.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    utils.login(request, user)
                    messages.success(request, 'Login successful')

                    redirect_url = request.GET.get('next', 'index')
                    return redirect(redirect_url)
                else:
                    messages.error(request, 'User is inactive')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'prosodyauth/login.html', {'form': form})

def logout(request):
    utils.logout(request)
    return redirect('index')

def register(request):
    if request.user.is_authenticated():
        messages.warning(request, 'You may not register a new account while logged in')
        return redirect('index')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'], is_active=False)
                    user.save()
                    confirmation = RegistrationConfirmation(user=user)
                    confirmation.save()
                    confirmation.password = binascii.hexlify(backend.salt_password(form.cleaned_data['password'], confirmation.token, confirmation.iterations))
                    confirmation.save()

                    #Build the URL for account activation
                    activation_url = request.build_absolute_uri(reverse('auth:activate', args=(confirmation.token,)))
                    #Build the context for our email templates
                    context = {'username': user.username, 'activation_url': activation_url}
                    #Now parse our plaintext and HTMLy templates
                    email_text = render_to_string('prosodyauth/email.txt', context)
                    email_html = render_to_string('prosodyauth/email.html', context)

                    #And, finally, send the email
                    send_mail('Activate your account', email_text, settings.EMAIL_SENDER, [user.email], html_message=email_html)

                messages.success(request, 'An activation email has been sent to your supplied email address')
                return redirect('index')
            except IntegrityError as e:
                messages.error(request, 'A database error occurred: {}'.format(str(e)))
    else:
        form = RegistrationForm()

    return render(request, 'prosodyauth/register.html', {'form': form})

def activate(request, token):
    try:
        activate = RegistrationConfirmation.objects.get(token=token)
        user = activate.user
    except RegistrationConfirmation.DoesNotExist:
        raise Http404("Activation token not found")

    return render(request, 'prosodyauth/activate.html', {'user': user})

