import datetime
import calendar


from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone


# Create your views here.
class EventsView(TemplateView):
    template_name = 'events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localtime(timezone.now())
        cal = calendar.Calendar(6)

        context['dates'] = cal.monthdatescalendar(2016,10)
        context['today'] = today

        return context

