from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator


from account.forms import PasswordChangeForm
from prosodyauth.mixins import LoginRequiredMixin

# Create your views here.

class AccountSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm()

        return render(request, 'account/settings.html', {'passform': form})
