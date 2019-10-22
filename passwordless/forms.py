from django import forms
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils import timezone


from passwordless.models import User, AuthToken
from simplecaptcha import captcha
from prosody.utils import nodeprep


from helpers.forms import PlaceholderFormMixin


@captcha
class LoginForm(PlaceholderFormMixin, forms.Form):
    username = forms.CharField(min_length=3, max_length=30, label="username or email")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            raise forms.ValidationError('User could not be found')

        return username

    def send_email(self):
        username = self.cleaned_data['username']
        user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        auth = AuthToken(user=user)
        auth.save()

        self.request.session['passwordless_session_key'] = auth.session_key

        #Build the URL for account authentication
        authn_url = self.request.build_absolute_uri(reverse('auth:authn', args=(auth.token,)))
        #Build the context for our email templates
        context = {
                'username': user.username,
                'email': user.email,
                'authn_url': authn_url,
                'sent': auth.date_sent,
                'expires': auth.date_expires,
        }
        #Now parse our plaintext and HTMLy templates
        email_text = render_to_string('passwordless/email.txt', context)
        email_html = render_to_string('passwordless/email.html', context)

        #And, finally, send the email
        email = EmailMultiAlternatives(
                'AKWriters: Log in now!',
                email_text,
                settings.EMAIL_SENDER,
                [user.email],
                headers={'X-Entity-Ref-ID': auth.token},
                )
        email.attach_alternative(email_html, 'text/html')
        email.send()

        messages.success(self.request, 'An email has been sent with instructions for logging in.')


class RegistrationForm(LoginForm):
    email = forms.EmailField()

    field_order = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'username'
        self.fields['username'].widget.attrs['placeholder'] = 'username'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            node = nodeprep(username)
        except UnicodeError:
            raise forms.ValidationError('Username contains invalid characters', code='invalid')

        self._purge_unvalidated_users()

        if User.objects.filter(Q(username__iexact=username) | Q(jid_node__iexact=node)).count() > 0:
            raise forms.ValidationError('That username is already taken', code='invalid')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('That email is already in use', code='invalid')

        return email

    def _purge_unvalidated_users(self):
        # Delete inactive User objects without an unexpired authtoken
        User.objects.filter(is_active=False).exclude(authtoken__date_expires__gte = timezone.now()).delete()

    def create_user(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        user = User(username=username, email=email)
        user.save()

