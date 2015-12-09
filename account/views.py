from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib import messages


from account.forms import PasswordChangeForm
from prosodyauth.mixins import LoginRequiredMixin
from prosodyauth.models import Prosody
from prosodyauth import authenticate


# Create your views here.

class AccountSettingsView(LoginRequiredMixin, View):
    _pass_form = None

    def get(self, request):
        return self._render_settings(request)

    def post(self, request):
        if request.GET['panel'] == 'password':
            self._change_password(request)
        else:
            messages.error(request, 'Invalid submission, please try again.')

        return self._render_settings(request)

    def _change_password(self, request):
        form = PasswordChangeForm(request.POST)

        # Validate the form, remembering to supply the user's username
        if form.is_valid(request.user.username):
            # Verify that it is this user's password
            account_store = Prosody.accounts.filter(user=request.user.username)
            account_data = dict()
            for item in account_store:
                account_data[item.key] = item.value

            # "Fix" the key that doesn't match our kwargs later
            account_data['iterations'] = account_data['iteration_count']
            del account_data['iteration_count']

            if authenticate.verify_password(password=form.cleaned_data['old_password'], **account_data):
                # Everything checks out, change the user's password
                user = request.user

                # A new salt will be generated and the password hashed
                user.password = form.cleaned_data['new_password']
                user.save()

                messages.success(request, 'Your password has been changed.')
            else:
                messages.error(request, 'You did not enter your correct password.')

        self._pass_form = form

    def _render_settings(self, request):
        form = self._pass_form or PasswordChangeForm()

        return render(request, 'account/settings.html', {'passform': form})
