from django.shortcuts import render


from account.forms import PasswordChangeForm
from prosodyauth.decorators import login_required

# Create your views here.

@login_required
def settings(request):
    form = PasswordChangeForm()

    return render(request, 'account/settings.html', {'passform': form})
