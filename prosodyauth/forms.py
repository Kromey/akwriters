from django import forms
from django.core.exceptions import ValidationError


from prosodyauth import fields
from prosodyauth.prosody.parsejid import nodeprep
from prosodyauth.models import User
from simplecaptcha import captcha


class PlaceholderForm(forms.Form):
    """
    A base form for automatically adding placeholder text.

    Forms that extend this form will by default have all text, password, and
    date input widgets display placeholder text equal to their label. This can
    be overridden per form field by simply specifying a different placeholder
    attribute.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.PasswordInput, forms.EmailInput, forms.DateInput):
                    field.widget.attrs.update(
                            { 'placeholder': field.widget.attrs.get('placeholder', field.label or field_name) }
                            )


class LoginForm(PlaceholderForm):
    username = forms.CharField(min_length=3, max_length=30)
    password = fields.PassField(min_length=8)

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
            username = nodeprep(username)
        except UnicodeError as err:
            raise ValidationError(str(err), code='invalid')

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

