from django import forms


from simplecaptcha import captcha


from helpers.forms import PlaceholderFormMixin, BootstrapFormMixin


@captcha
class RegistrationForm(PlaceholderFormMixin, forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField()

