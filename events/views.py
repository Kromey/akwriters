import datetime
import calendar


from django.shortcuts import render
from django.views.generic import TemplateView,RedirectView
from django.utils import dateparse,timezone


from .models import Calendar,MonthCache
from . import utils


# Create your views here.
class CalendarCssView(TemplateView):
    template_name = 'events/calendars.css'
    content_type = 'text/css'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendars'] = Calendar.objects.all()

        return context


class EventsView(TemplateView):
    template_name = 'events/index.html'

    year = None
    month = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localtime(timezone.now()).date()
        try:
            self.year = int(self.kwargs['year'])
            self.month = int(self.kwargs['month'])
        except KeyError:
            self.year = today.year
            self.month = today.month

        current_month = datetime.date(self.year, self.month, 1)
        dates = calendar.Calendar(6).monthdatescalendar(current_month.year, current_month.month)

        events = {}
        gcals = Calendar.objects.all()
        for gcal in gcals:
            gdata = gcal.get_events(current_month)

            for event in gdata['items']:
                event['css_class'] = gcal.css_class
                try:
                    startdate = dateparse.parse_datetime(event['start']['dateTime'])
                    enddate = dateparse.parse_datetime(event['end']['dateTime'])

                    event['start_time'] = startdate.time()
                    event['end_time'] = enddate.time()

                    startdate = startdate.date()
                    enddate = enddate.date()
                except KeyError:
                    startdate = dateparse.parse_date(event['start']['date'])
                    enddate = dateparse.parse_date(event['end']['date'])

                event['start_date'] = startdate
                event['end_date'] = enddate

                try:
                    events[startdate.isoformat()].append(event)
                except KeyError:
                    events[startdate.isoformat()] = [event,]

        cal = []
        for week in dates:
            cal.append([])
            for date in week:
                isodate = date.isoformat()
                date_events = events.get(isodate, [])
                date_events.sort(key=utils.event_key)

                cal[-1].append({
                    'date': date,
                    'events': date_events,
                    })

        context['calendar'] = cal
        context['gcals'] = gcals
        context['current_month'] = current_month
        context['last_month'] = current_month - datetime.timedelta(days=1)
        context['next_month'] = current_month + datetime.timedelta(days=32)
        context['today'] = today

        return context

