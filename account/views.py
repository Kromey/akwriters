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
    _pass_form_data = None

    def get(self, request):
        return self._render_settings(request)

    def post(self, request):
        # TODO: Will need some kind of switch to determine what we're doing
        self._change_password(request)

        return self._render_settings(request)

    def _change_password(self, request):
        # Ensure the logged-in user's username is here; needed for validation
        post_data = request.POST.copy()
        post_data['username'] = request.user.username
        form = PasswordChangeForm(post_data)

        messages.debug(request, post_data)
        if form.is_valid():
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

        self._pass_form_data = post_data

    def _render_settings(self, request):
        form = PasswordChangeForm(self._pass_form_data)

        return render(request, 'account/settings.html', {'passform': form})
