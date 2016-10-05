from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView


from passwordless.models import AuthToken


# Create your views here.
class CandyView(TemplateView):
    template_name = 'chat/candy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        auth = AuthToken(user=self.request.user)
        auth.save()

        context['otp'] = auth.token

        return context

