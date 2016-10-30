from django.conf.urls import include, url


from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^characters$', views.CharacterListView.as_view(), name='character_list'),
    url(r'^characters/new$', views.CharacterCreateView.as_view(), name='character_create'),
]
