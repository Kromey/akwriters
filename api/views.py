from django.shortcuts import render
from django.views.generic import View


from .utils import ApiResponse

# Create your views here.

class StatusView(View):
    def get(self, request):
        status = {'status': 'The Website is UP! :)'}
        return ApiResponse(status)
