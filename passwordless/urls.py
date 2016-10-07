from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'akwriters.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name='logout'),
    url(r'^register', views.RegisterView.as_view(), name='register'),
    url(r'^n/(?P<token>[0-9a-zA-Z]+)$', views.AuthnView.as_view(), name='authn'),
    url(r'^api/json$', csrf_exempt(views.ApiAuthView.as_view()), name='api_json'),
    url(r'^apppasswords$', views.AppPasswordListView.as_view(), name='apppasswords'),
    url(r'^apppasswords/revoke$', views.AppPasswordRevokeView.as_view(), name='revoke_apppassword'),
]
