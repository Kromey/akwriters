from datetime import datetime, timedelta
import jwt
import os


from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView


key = os.path.join(
    os.path.dirname(__file__),
    'ecc',
    'key.pem',
)
with open(key, 'r') as fh:
    ecc_private = fh.read()


# Create your views here.
class NabuView(TemplateView):
    template_name = 'chat/nabu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = {
            'sub': 'Kromey',
            'iss': self.request.headers['Host'],
            'aud': self.request.headers['Host'],
            'exp': datetime.utcnow() + timedelta(seconds=30),
        }
        token = jwt.encode(data, ecc_private, algorithm='ES256')
        context['token'] = token.decode('utf-8')

        return context

