from django.conf.urls import include, url
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', TemplateView.as_view(template_name='chat/index.html'), name='index'),
    url(r'^pidgin$', TemplateView.as_view(template_name='chat/pidgin.html'), name='pidgin'),
    url(r'^adium$', TemplateView.as_view(template_name='chat/adium.html'), name='adium'),
    url(r'^annika$', TemplateView.as_view(template_name='chat/annika.html'), name='annika'),
    url(r'^candy$', views.CandyView.as_view(), name='candy'),
]
