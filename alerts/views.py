from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def test(request):
    messages.set_level(request, messages.DEBUG)

    messages.debug(request, 'This is a debug alert')
    messages.info(request, 'This is an info alert')
    messages.success(request, 'This is a success alert')
    messages.warning(request, 'This is a warning alert')
    messages.error(request, 'This is an error alert')

    return render(request, 'alerts/test.html')
