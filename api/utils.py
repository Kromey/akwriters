import json


from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers


class ApiResponse(HttpResponse):
    """JSON-encoded API response

    I've arbitrarily decided that the API uses JSON responses. To ease the
    encoding process and to ensure that the correct Content-Type is set, this
    object simply takes an encodable data object and returns an HttpResponse
    object that properly encapsulates it as JSON.
    """

    def __init__(self, data):
        """Build a JSON-encoded API response."""
        jdata = json.dumps(data, separators=(',', ':'))
        super().__init__(jdata, content_type="application/json")

def apimethod(method):
    """Decorator for an API method to properly handle encoding API responses.

    The decorated method is expected to return a Python object that can be
    encoded into JSON; it will then be magically transformed into one that
    returns properly-encoded JSON."""
    def wrapper(*args, **kwargs):
        data = {
                "meta": {
                    "status": "OK",
                    },
                "response": {}
                }

        try:
            data["response"] = method(*args, **kwargs)
        except Exception as e:
            data["meta"]["status"] = "ERR"
            data["meta"]["error"] = str(e)

        response = ApiResponse(data)
        # Ensure API responses are never cached
        add_never_cache_headers(response)

        return response

    return wrapper

