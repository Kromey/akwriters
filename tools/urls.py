from django.conf.urls import include, url
from django.urls import path


from . import views

app_name = 'tools'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('stories/', views.StoryListView.as_view(), name='story_list'),
    url(r'^characters$', views.CharacterListView.as_view(), name='character_list'),
    url(r'^characters/new$', views.CharacterCreateView.as_view(), name='character_create'),
    url(r'^characters/view/(?P<pk>[\d]+)$', views.CharacterDetailView.as_view(), name='character_detail'),
    url(r'^characters/edit/(?P<pk>[\d]+)$', views.CharacterEditView.as_view(), name='character_edit'),
    url(r'^characters/notes/(?P<pk>[\d]+)$', views.CharacterNotesView.as_view(), name='character_notes'),
]
