from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^auth/', include('prosodyauth.urls')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^policies/', include('policies.urls', namespace='policies')),
)
