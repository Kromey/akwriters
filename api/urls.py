from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from .views import StatusView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^status$', StatusView.as_view(), name='status'),
)
