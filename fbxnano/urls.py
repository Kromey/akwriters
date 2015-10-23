from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^events$', TemplateView.as_view(template_name='events.html'), name='events'),
    url(r'^auth/', include('prosodyauth.urls', namespace='auth')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^policies/', include('policies.urls', namespace='policies')),
)
