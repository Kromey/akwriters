from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('resources', TemplateView.as_view(template_name='resources.html'), name='resources'),
    path('events/', include('events.urls', namespace='events')),
    #path(r'^account/', include('account.urls', namespace='account')),
    path('alerts/', include('alerts.urls', namespace='alerts')),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('passwordless.urls', namespace='auth')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('favicon/', include('favicon.urls', namespace='favicon')),
    path('policies/', include('policies.urls', namespace='policies')),
    path('tools/', include('tools.urls', namespace='tools')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('admin/', admin.site.urls),
]
