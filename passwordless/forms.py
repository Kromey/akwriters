from django import forms
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse


from passwordless.models import User, AuthToken
from simplecaptcha import captcha


from helpers.forms import PlaceholderFormMixin


@captcha
class LoginForm(PlaceholderFormMixin, forms.Form):
    username = forms.CharField(min_length=3, max_length=30, label="username or email")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            try:
                User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                raise forms.ValidationError('User could not be found')

        return username

    def send_email(self):
        username = self.cleaned_data['username']
        user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        auth = AuthToken(user=user)
        auth.save()

        #Build the URL for account authentication
        authn_url = reverse('auth:authn', args=(auth.token,))
        #Build the context for our email templates
        context = {'username': user.username, 'authn_url': authn_url}
        #Now parse our plaintext and HTMLy templates
        email_text = render_to_string('passwordless/email.txt', context)
        email_html = render_to_string('passwordless/email.html', context)

        #And, finally, send the email
        send_mail('Activate your account', email_text, settings.EMAIL_SENDER, [user.email], html_message=email_html)


class RegistrationForm(LoginForm):
    email = forms.EmailField()

    field_order = ['username','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'username'
        self.fields['username'].widget.attrs['placeholder'] = 'username'

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username__iexact=username).count() > 0:
            raise forms.ValidationError('That username is already taken', code='invalid')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('That email is already in use', code='invalid')

        return email

    def create_user(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        user = User(username=username, email=email)
        user.save()

