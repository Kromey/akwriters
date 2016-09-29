from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.edit import FormView


from . import forms
from . import models

# Create your views here.
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
        user = authenticate(token=token)
        if user is not None:
            login(request, user)
            return redirect('chat:index')
        else:
            if request.user.is_authenticated:
                messages.info(request, 'You are already authenticated on this site')
                return redirect('chat:index')
            else:
                return render(request, 'passwordless/invalid.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

