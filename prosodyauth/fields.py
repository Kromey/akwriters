from django import forms


class PassField(forms.CharField):
    widget = forms.PasswordInput

