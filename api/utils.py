import json


from django.http import HttpResponse


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

