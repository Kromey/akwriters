from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'passwordless/login.html')

def logout(request):
    return render(request, 'passwordless/logout.html')

def register(request):
    return render(request, 'passwordless/register.html')

def authn(request, token):
    return render(request, 'passwordless/authn.html')

