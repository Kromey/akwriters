from django import forms
from django.core.exceptions import ValidationError


from formhelpers.forms import PlaceholderForm
from simplecaptcha import captcha


contact_reasons = (
        ('question', 'Question'),
        ('problem', 'Problem'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other'),
        )

class ContactForm(PlaceholderForm):
    username = forms.CharField(widget=forms.HiddenInput, required=False)
    # ip_address = forms.GenericIPAddressField(widget=forms.HiddenInput)
    reason = forms.ChoiceField(choices=contact_reasons)
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

