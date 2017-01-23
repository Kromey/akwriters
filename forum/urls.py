from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', views.IndexView.as_view(), name='index'),
    url('^board/(?P<slug>[-\w]+)/$', views.BoardView.as_view(), name='board'),
    url('^board/(?P<board>[-\w]+)/post/(?P<pk>[0-9]+)$', views.PostView.as_view(), name='post'),
]
