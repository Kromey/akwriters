from django.conf.urls import include, url


from .views import AccountSettingsView


urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^settings', AccountSettingsView.as_view(), name='settings'),
]
