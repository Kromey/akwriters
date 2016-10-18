import datetime
import calendar
import json
from urllib import request,parse


from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import dateparse,timezone


from .models import Calendar


# Create your views here.
class EventsView(TemplateView):
    template_name = 'events/index.html'

    year = None
    month = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localtime(timezone.now())
        try:
            self.year = int(self.kwargs['year'])
            self.month = int(self.kwargs['month'])
        except KeyError:
            self.year = today.year
            self.month = today.month

        current_month = datetime.date(self.year, self.month, 1)
        dates = calendar.Calendar(6).monthdatescalendar(current_month.year, current_month.month)

        # Set boundary dates at 1w before and after our current view
        # 1w is probably overkill, but handles timezones and long events
        time_min = dates[0][0] - datetime.timedelta(weeks=1)
        time_min = time_min.isoformat() + 'T00:00:00Z'
        time_max = dates[-1][-1] + datetime.timedelta(weeks=1)
        time_max = time_max.isoformat() + 'T00:00:00Z'

        # This needs to use an API key from Google
        api_key = settings.GCAL_API_KEY

        events = {}
        gcals = Calendar.objects.all()
        for gcal in gcals:
            url = 'https://www.googleapis.com/calendar/v3/calendars/{calendar}/events?singleEvents=true&timeMin={time_min}&timeMax={time_max}&key={api_key}'.format(
                    calendar=parse.quote(gcal.remote_id),
                    time_min=parse.quote(time_min),
                    time_max=parse.quote(time_max),
                    api_key=parse.quote(api_key),
                    )

            rawdata = request.urlopen(url).read()
            gdata = json.loads(rawdata.decode('utf8'))

            for event in gdata['items']:
                event['css_class'] = gcal.css_class
                try:
                    date = dateparse.parse_datetime(event['start']['dateTime']).date().isoformat()
                except KeyError:
                    date = dateparse.parse_date(event['start']['date']).isoformat()

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
        context['gcals'] = gcals
        context['current_month'] = current_month
        context['last_month'] = current_month - datetime.timedelta(days=1)
        context['next_month'] = current_month + datetime.timedelta(days=32)
        context['today'] = today

        return context

