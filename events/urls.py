from django.conf.urls import include, url


from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', views.EventsView.as_view(), name='index'),
    url('^(?P<year>[\d]{4})(?P<month>[\d]{2})$', views.EventsView.as_view(), name='index'),
]
