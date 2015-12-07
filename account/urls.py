from django.conf.urls import patterns, include, url


from .views import AccountSettingsView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fbxnano.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^settings', AccountSettingsView.as_view(), name='settings'),
)
