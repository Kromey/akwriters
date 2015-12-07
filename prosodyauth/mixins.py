from .decorators import login_required


class LoginRequiredMixin(object):
    """Mixin to require authentication for all methods.

    Use this as a mixin for class-based views to require that all methods of
    accessing it require authentication, identical to the login_required
    decorator also available in this module.
    """
    @classmethod
    def as_view(cls, *args, **kwargs):
        """Access to the object as a view requiring authentication."""
        view = super().as_view(*args, **kwargs)
        return login_required(view)
