from django.shortcuts import render
from django.views.generic.edit import FormView


from . import forms

# Create your views here.
def login(request):
    return render(request, 'passwordless/login.html')

def logout(request):
    return render(request, 'passwordless/logout.html')

def authn(request, token):
    return render(request, 'passwordless/authn.html')


class RegisterView(FormView):
    template_name = 'passwordless/register.html'
    form_class = forms.RegistrationForm
    success_url = '/'

