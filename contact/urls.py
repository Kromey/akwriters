from django.conf.urls import include, url

from . import views

app_name = 'contact'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.contact, name='contact'),
]
