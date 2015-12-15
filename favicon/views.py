from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.

_icon_sizes = (36, 48, 72, 96, 144, 192)
def manifest(request):
    manifest_data = {}
    manifest_data['name'] = 'Alaska Writers'

    icon_data = []

    for size in _icon_sizes:
        """
        "src": "\/static\/favicons\/android-chrome-36x36.png",
        "sizes": "36x36",
        "type": "image\/png",
        "density": "0.75"
        """
        size = str(size)

        icon = {}

        icon_file = 'android-chrome-{size}x{size}.png'.format(size=size)
        icon['src'] = static('favicon/{file}'.format(file=icon_file))

        icon['sizes'] = '{size}x{size}'.format(size=size)
        icon['type'] = 'image/png'
        icon['density'] = '0.75'

        icon_data.append(icon)

    manifest_data['icons'] = icon_data

    return JsonResponse(manifest_data)

def browserconfig(request):
    return render(request, 'favicon/browserconfig.xml', content_type='application/xml')
