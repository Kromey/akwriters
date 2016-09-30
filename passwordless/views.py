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
        session_key = request.session.pop('passwordless_session_key', None)

        user = authenticate(token=token, session_key=session_key)
        if user is not None:
            login(request, user)

            if not user.is_active:
                # Activate the user
                user.is_active = True
                user.save()

                messages.success(request, 'Your account is now active on this site')

            return redirect('chat:index')
        else:
            if request.user.is_authenticated:
                messages.info(request, 'You are already authenticated on this site')
                return redirect('chat:index')
            else:
                # Put the session key back, just in case user used wrong email
                if session_key is not None:
                    request.session['passwordless_session_key'] = session_key

                return render(request, 'passwordless/invalid.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out of the site')
        return redirect('index')

