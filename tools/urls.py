from django.urls import path, re_path
from django.views.generic import RedirectView


from . import views

app_name = 'tools'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('stories/', views.StoryListView.as_view(), name='story_list'),
    path('stories/<int:pk>/', views.StoryDetailView.as_view(), name='story_detail'),

    path('stories/<int:story_id>/characters/<int:pk>', views.CharacterDetailView.as_view(), name='character_detail'),
    path('stories/<int:story_id>/characters/<int:pk>/edit', views.CharacterEditView.as_view(), name='character_edit'),
    path('stories/<int:story_id>/characters/<int:pk>/notes', views.CharacterNotesView.as_view(), name='character_notes'),
    path('stories/<int:story_id>/characters/new', views.CharacterCreateView.as_view(), name='character_create'),

    re_path(r'^characters(?:/.*)?$', RedirectView.as_view(pattern_name='tools:story_list')),
]
