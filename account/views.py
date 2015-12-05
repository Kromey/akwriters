from django.shortcuts import render


from account.forms import PasswordChangeForm

# Create your views here.

def settings(request):
    form = PasswordChangeForm()

    return render(request, 'account/settings.html', {'passform': form})
