from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator


from account.forms import PasswordChangeForm
from prosodyauth.decorators import login_required

# Create your views here.

class AccountSettingsView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PasswordChangeForm()

        return render(request, 'account/settings.html', {'passform': form})
