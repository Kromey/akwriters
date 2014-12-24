from django.middleware.csrf import rotate_token


from prosodyauth.models import User, AnonymousUser
from prosodyauth.prosody.backend import ProsodyBackend


SESSION_KEY = '_prosodyauth_user_id'


def login(request, user):
    try:
        user_id = request.session[SESSION_KEY]
        if user.pk != user_id:
            #We're logging in as a different user, start a clean session
            request.session.flush()
    except KeyError:
        #Logging in a formerly-anonymous session, change the key but keep session data
        request.session.cycle_key()

    request.session[SESSION_KEY] = user.pk
    request.user = user
    rotate_token(request)

def logout(request):
    request.session.flush()
    request.user = AnonymousUser()

def get_user(request):
    user = None

    try:
        user_id = request.session[SESSION_KEY]
    except KeyError:
        pass
    else:
        backend = ProsodyBackend()
        user = backend.get_user(user_id)
        # TODO: Verify the session?

    return user or AnonymousUser()

