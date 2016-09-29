from django import forms


from passwordless.models import User
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

