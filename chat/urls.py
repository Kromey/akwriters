from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


from . import views

app_name = 'chat'
urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('', TemplateView.as_view(template_name='chat/index.html'), name='index'),
    path('nabu', login_required(views.NabuView.as_view()), name='nabu'),
    #url(r'^candy$', login_required(views.CandyView.as_view()), name='candy'),
]
