from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^manifest.json$', 'favicon.views.manifest', name='manifest'),
    url(r'^browserconfig.xml$', 'favicon.views.browserconfig', name='browserconfig'),
)