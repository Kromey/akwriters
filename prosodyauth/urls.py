from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login', 'prosodyauth.views.login', name='login'),
    url(r'^logout', 'prosodyauth.views.logout', name='logout'),
    url(r'^register', 'prosodyauth.views.register', name='register'),
    url(r'^activate/(?P<token>[0-9a-zA-Z]+)', 'prosodyauth.views.activate', name='activate'),
)
