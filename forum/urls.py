from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', views.BoardView.as_view(), name='index'),
]
