from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^events$', TemplateView.as_view(template_name='events.html'), name='events'),
    url(r'^links$', TemplateView.as_view(template_name='links.html'), name='links'),
    #url(r'^account/', include('account.urls', namespace='account')),
    url(r'^alerts/', include('alerts.urls', namespace='alerts')),
    url(r'^api/', include('api.urls', namespace='api')),
    #url(r'^auth/', include('prosodyauth.urls', namespace='auth')),
    url(r'^auth/', include('passwordless.urls', namespace='auth')),
    url(r'^chat/', include('chat.urls', namespace='chat')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^favicon/', include('favicon.urls', namespace='favicon')),
    url(r'^policies/', include('policies.urls', namespace='policies')),
    url(r'^admin/', admin.site.urls),
]
