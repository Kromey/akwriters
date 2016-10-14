from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class EventsView(TemplateView):
    template_name = 'events/index.html'

