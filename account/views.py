from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib import messages


from account.forms import PasswordChangeForm
from prosodyauth.mixins import LoginRequiredMixin

# Create your views here.

class AccountSettingsView(LoginRequiredMixin, View):
    _pass_form_data = None

    def get(self, request):
        return self._render_settings(request)

    def post(self, request):
        # Ensure the logged-in user's username is here; needed for validation
        post_data = request.POST.copy()
        post_data['username'] = request.user.username
        form = PasswordChangeForm(post_data)

        messages.debug(request, post_data)
        if form.is_valid():
            messages.success(request, 'You have correctly entered a password')
        else:
            messages.error(request, 'You have incorrectly entered a password')

        self._pass_form_data = post_data
        return self._render_settings(request)

    def _render_settings(self, request):
        form = PasswordChangeForm(self._pass_form_data)

        return render(request, 'account/settings.html', {'passform': form})
