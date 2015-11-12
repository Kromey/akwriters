from django.shortcuts import render
from django.views.generic import View


from .utils import apimethod

# Create your views here.

class StatusView(View):
    @apimethod
    def get(self, request):
        return {
                'web': 'UP', #Tautological: If we're responding, we're up
                'xmpp': 'UNK', #TODO: Check if it's up
                }
