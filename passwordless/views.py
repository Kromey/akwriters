from django.shortcuts import render
from django.views.generic.edit import FormView


from . import forms

# Create your views here.
def logout(request):
    return render(request, 'passwordless/logout.html')

def authn(request, token):
    return render(request, 'passwordless/authn.html')


class LoginView(FormView):
    template_name = 'passwordless/login.html'
    form_class = forms.LoginForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()

        return super().form_valid(form)


class RegisterView(LoginView):
    template_name = 'passwordless/register.html'
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        form.create_user()

        return super().form_valid(form)

