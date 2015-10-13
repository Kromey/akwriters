from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^privacy$', TemplateView.as_view(template_name='policies/privacy.html'), name='privacy'),
)
