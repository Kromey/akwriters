from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {'domain': settings.PROSODY_DEFAULT_DOMAIN})

def pidgin(request):
    return render(request, 'chat/pidgin.html', {'domain': settings.PROSODY_DEFAULT_DOMAIN})

def adium(request):
    return render(request, 'chat/adium.html', {'domain': settings.PROSODY_DEFAULT_DOMAIN})

