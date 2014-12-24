from django.utils.functional import SimpleLazyObject


from prosodyauth.utils import get_user


class AuthenticationMiddleware:
    def __init__(self):
        pass

    def process_request(self, request):
        assert hasattr(request, 'session'), (
                "The prosodyauth authentication system requires Django's session middleware be enabled"
                )
        request.user = SimpleLazyObject(lambda: get_user(request))

