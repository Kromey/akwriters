import json


from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic.edit import FormView,CreateView
from django.views.generic.list import ListView


from . import forms
from . import models
from prosody.models import ProsodyRoster

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

                # Now let's add the bot to the user's roster
                data = {
                        'name': settings.THE_BOT['name'],
                        'ask': 'subscribe',
                        'subscription': 'none',
                        'groups': {'Nano': True },
                }

                roster = ProsodyRoster(user=user.username, key=settings.THE_BOT['jid'])
                roster.encode(data)
                roster.save()

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


class ApiAuthView(View):
    def post(self, request):
        req = json.loads(request.body.decode('utf8'))
        user = authenticate(token=req['password'], username=req['username'])

        if user is not None:
            return HttpResponse('true', content_type='text/plain')
        else:
            user = authenticate(username=req['username'], password=req['password'])
            if user is not None:
                return HttpResponse('true', content_type='text/plain')
            else:
                return HttpResponseForbidden('false', content_type='text/plain')


class AppPasswordListView(LoginRequiredMixin, ListView):
    model = models.AppPassword
    context_object_name = 'password_list'

    def get_queryset(self):
        return self.request.user.apppassword_set.all()


class AppPasswordRevokeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            models.AppPassword.objects.get(user=request.user, pk=request.POST['password-id']).delete()
        except models.AppPassword.DoesNotExist:
            messages.error(request, 'Could not delete the requested password.')

        return redirect('auth:apppasswords')


class AppPasswordCreateView(LoginRequiredMixin, View):
    def post(self, request):
        ap = models.AppPassword(user=request.user, name=request.POST['new_password_name'])
        password = ap.password # Have to retrieve this before we save
        ap.save()

        if request.is_ajax():
            template = 'passwordless/apppassword_new_content.html'
        else:
            template = 'passwordless/apppassword_new.html'
        return render(request, template, context={'password':password,'name':ap.name})

