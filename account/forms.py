from django import forms
from django.core.exceptions import ValidationError


from prosodyauth import fields, authenticate


from helpers.forms import PlaceholderForm


class PasswordChangeForm(PlaceholderForm):
    old_password = fields.PassField(min_length=8, label='current password')
    new_password = fields.PassField(min_length=8, label='new password')
    new_password_confirm = fields.PassField(label='confirm password')

    # Used for validation
    _username = None

    def is_valid(self, username, *args, **kwargs):
        """Validation of this form requires the user's username be supplied."""
        self._username = username
        super().is_valid(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm = cleaned_data.get('new_password_confirm')

        if password and password != confirm:
            self.add_error('new_password_confirm', ValidationError('Confirmation must match password', code='invalid'))
        elif password and not authenticate.password_is_compliant(password, self._username):
            self.add_error('new_password', ValidationError('Password does not meet requirements', code='invalid'))

class EmailChangeForm(PlaceholderForm):
    email = forms.EmailField(label='new email address')
    email_confirm = forms.EmailField(label='confirm email address')

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('email') != cleaned_data.get('email_confirm'):
            self.add_error('email_confirm', ValidationError('Emails do not match', code='invalid'))

