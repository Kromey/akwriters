from django import forms
from django.core.exceptions import ValidationError


from prosodyauth import fields, authenticate
from prosodyauth.prosody.parsejid import nodeprep
from prosodyauth.models import User
from simplecaptcha import captcha


from helpers.forms import PlaceholderForm


class LoginForm(PlaceholderForm):
    username = forms.CharField(min_length=3, max_length=30)
    password = fields.PassField(min_length=8)
    next_url = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_username(self):
        """Normalize the username field by stripping '@domain' part

        Users may end up with their JID ('username@domain.tld') in their
        browser's stored passwords, which then can obstruct their ability to
        log into the website. This is easily remedied by simply stripping out
        any '@domain.tld' attached to the username when logging in.
        """
        username = self.cleaned_data.get('username')

        # Might be best to only strip out our XMPP domain, but this works too
        return username.split('@')[0]

    def render_password(self, render_value=True):
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) == forms.PasswordInput:
                    field.widget.render_value = render_value

@captcha
class RegistrationForm(LoginForm):
    email = forms.EmailField()
    password_confirm = fields.PassField(label='confirm password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            node = nodeprep(username)
        except UnicodeError as err:
            raise ValidationError(str(err), code='invalid')

        if node.lower() != username.lower():
            raise ValidationError('That username contains invalid characters', code='invalid')

        if User.objects.filter(username__iexact=username).count() > 0:
            raise ValidationError('That username is already taken', code='invalid')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if User.objects.filter(email=email).count() > 0:
            raise ValidationError('That email is already in use', code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('password_confirm')

        if password and password != confirm:
            self.add_error('password_confirm', ValidationError('Confirmation must match password', code='invalid'))
        elif password and not authenticate.password_is_compliant(password, cleaned_data.get('username')):
            self.add_error('password', ValidationError('Password does not meet requirements', code='invalid'))

class ResendActivationForm(PlaceholderForm):
    user = forms.CharField(label='username or email')

