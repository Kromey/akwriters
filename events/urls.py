from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views

app_name = 'events'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', views.EventsView.as_view(), name='index'),
    url('^(?P<year>[\d]{4})(?P<month>[\d]{2})$', views.EventsView.as_view(), name='index'),
    url('^calendars.css$', views.CalendarCssView.as_view(), name='calendars_css'),
]
