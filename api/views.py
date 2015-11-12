from django.shortcuts import render
from django.views.generic import View


from .utils import apimethod

# Create your views here.

class StatusView(View):
    @apimethod
    def get(self, request):
        return {'status': 'The Website is UP! :)'}
