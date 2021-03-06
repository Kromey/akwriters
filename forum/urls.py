from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views

app_name = 'forum'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', views.IndexView.as_view(), name='index'),
    url('^search$', views.SearchView.as_view(), name='search'),
    url('^preview$', views.PreviewView.as_view(), name='preview'),

    url('^(?P<slug>[-\w]+)/$', views.BoardView.as_view(), name='board'),
    url('^(?P<slug>[-\w]+)/page-(?P<page>[0-9]+)$', views.BoardView.as_view(), name='board'),
    url('^(?P<board>[-\w]+)/post-(?P<pk>[0-9]+)$', views.PostView.as_view(), name='post'),

    url('^(?P<board>[-\w]+)/new$', views.TopicCreateView.as_view(), name='new-topic'),
    url('^(?P<board>[-\w]+)/post-(?P<post>[0-9]+)/reply$', views.ReplyCreateView.as_view(), name='new-reply'),
]
