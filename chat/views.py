from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {'domain': settings.PROSODY_DEFAULT_DOMAIN})
