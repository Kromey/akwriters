from django.contrib import messages


from prosodyauth.views import login


def login_required(view_func):
    """Decorator for a view that requires a user to be logged in.

    """
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        # Fell through, that means user was not authenticated
        messages.error(request, 'You must be logged in to access this page')
        return login(request)

    return wrapped_view

