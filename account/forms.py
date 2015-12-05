from django import forms
from django.core.exceptions import ValidationError


from prosodyauth import fields, authenticate


from helpers.forms import PlaceholderForm


class PasswordChangeForm(PlaceholderForm):
    old_password = fields.PassField(min_length=8, label='current password')
    new_password = fields.PassField(min_length=8, label='new password')
    new_password_confirm = fields.PassField(label='confirm password')

    def render_password(self, render_value=True):
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) == forms.PasswordInput:
                    field.widget.render_value = render_value

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('password_confirm')

        if password and password != confirm:
            self.add_error('password_confirm', ValidationError('Confirmation must match password', code='invalid'))
        elif password and not authenticate.password_is_compliant(password, cleaned_data.get('username')):
            self.add_error('password', ValidationError('Password does not meet requirements', code='invalid'))

