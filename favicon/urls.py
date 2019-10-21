from django.conf.urls import include, url

from . import views

app_name = 'favicon'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^manifest.json$', views.manifest, name='manifest'),
    url(r'^browserconfig.xml$', views.browserconfig, name='browserconfig'),
]
