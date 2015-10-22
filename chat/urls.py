from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', 'chat.views.index', name='index'),
    url(r'^pidgin$', 'chat.views.pidgin', name='pidgin'),
    url(r'^adium$', 'chat.views.adium', name='adium'),
    url(r'^annika$', 'chat.views.annika', name='annika'),
)
