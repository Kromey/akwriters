import datetime
import json
from urllib import request,parse


from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Calendar(models.Model):
    name = models.CharField(max_length=30, unique=True)
    remote_id = models.CharField(max_length=60)
    css_class = models.CharField(max_length=10)

    def get_events(self, month):
        cache, created = MonthCache.objects.get_or_create(calendar=self, month=month)
        return cache.data

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


class MonthCache(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    month = models.DateField()
    data_cache = models.TextField()
    data_cached_on = models.DateTimeField()

    _base_url = 'https://www.googleapis.com/calendar/v3/calendars/{calendar}/events?singleEvents=true&timeMin={time_min}&timeMax={time_max}&key={api_key}'
    _cache_expires = datetime.timedelta(minutes=settings.GAPI_CACHE_EXPIRES)

    @property
    def url(self):
        # Normalize self.month to the first of the month
        self.month = datetime.date(self.month.year, self.month.month, 1)

        # Extend beyond the month to ensure we have everything we want to display
        time_min = self.month - datetime.timedelta(days=7)
        time_max = self.month + datetime.timedelta(days=37)

        # Need ISO format including time
        time_min = time_min.isoformat() + 'T00:00:00Z'
        time_max = time_max.isoformat() + 'T00:00:00Z'

        return self._base_url.format(
                calendar=parse.quote(self.calendar.remote_id),
                time_min=parse.quote(time_min),
                time_max=parse.quote(time_max),
                api_key=parse.quote(settings.GCAL_API_KEY),
                )

    @property
    def is_cache_stale(self):
        if self.data_cache is None:
            return True
        elif self.data_cached_on is None:
            return True
        elif self.data_cached_on + self._cache_expires < timezone.now():
            return True

        return False

    @property
    def data(self):
        return self._get_data(auto_save=True)

    def _get_data(self, auto_save):
        url = self.url

        if self.is_cache_stale:
            self.data_cache = request.urlopen(url).read().decode('utf8')
            self.data_cached_on = timezone.now()

            if auto_save:
                self.save()

        return json.loads(self.data_cache)

    def __str__(self):
        if self.is_cache_stale:
            return "{calendar} ({month}) [STALE]".format(
                    calendar=self.calendar,
                    month=self.month.isoformat()[:7]
                    )
        else:
            return "{calendar} ({month})".format(
                    calendar=self.calendar,
                    month=self.month.isoformat()[:7]
                    )

    def save(self, *args, **kwargs):
        self._get_data(auto_save=False)
        super().save(*args, **kwargs)


