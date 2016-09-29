from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView


from . import forms
from . import models

# Create your views here.
def logout(request):
    return render(request, 'passwordless/logout.html')


class LoginView(FormView):
    template_name = 'passwordless/login.html'
    form_class = forms.LoginForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.send_email()

        return super().form_valid(form)


class RegisterView(LoginView):
    template_name = 'passwordless/register.html'
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        form.create_user()

        return super().form_valid(form)


class AuthnView(View):
    def get(self, request, token):
        auth = models.AuthToken.objects.get(token=token)
        user = auth.user

        return render(request, 'passwordless/authn.html', {'auth_user':user, 'token':auth.token})

