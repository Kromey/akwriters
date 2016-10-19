import datetime
import json
from urllib import request,parse


from django.conf import settings
from django.db import models

# Create your models here.
class Calendar(models.Model):
    name = models.CharField(max_length=30, unique=True)
    remote_id = models.CharField(max_length=60)
    css_class = models.CharField(max_length=10)

    def json_data(self, time_min, time_max):
        url = 'https://www.googleapis.com/calendar/v3/calendars/{calendar}/events?singleEvents=true&timeMin={time_min}&timeMax={time_max}&key={api_key}'.format(
                calendar=parse.quote(self.remote_id),
                time_min=parse.quote(time_min),
                time_max=parse.quote(time_max),
                api_key=parse.quote(settings.GCAL_API_KEY),
                )

        rawdata = request.urlopen(url).read()
        return json.loads(rawdata.decode('utf8'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]

