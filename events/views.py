import datetime
import calendar
import json
from urllib import request,parse


from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import dateparse,timezone


# Create your views here.
class EventsView(TemplateView):
    template_name = 'events/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localtime(timezone.now())
        dates = calendar.Calendar(6).monthdatescalendar(today.year, today.month)

        time_min = dates[0][0].isoformat() + 'T00:00:00Z'
        api_key = settings.GCAL_API_KEY
        url = 'https://www.googleapis.com/calendar/v3/calendars/{calendar}/events?timeMin={time_min}&key={api_key}'.format(
                calendar=parse.quote('de0dm8l2ah81c1lvuqeq987480@group.calendar.google.com'),
                time_min=parse.quote(time_min),
                api_key=parse.quote(api_key),
                )

        rawdata = request.urlopen(url).read()
        gdata = json.loads(rawdata.decode('utf8'))

        events = {}
        for event in gdata['items']:
            date = dateparse.parse_datetime(event['start']['dateTime']).date().isoformat()
            try:
                events[date].append(event)
            except KeyError:
                events[date] = [event,]

        cal = []
        for week in dates:
            cal.append([])
            for date in week:
                isodate = date.isoformat()
                cal[-1].append({
                    'date': date,
                    'events': events.get(isodate, [])
                    })

        context['calendar'] = cal
        context['today'] = today

        return context

