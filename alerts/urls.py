from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^test', 'alerts.views.test', name='test'),
)
