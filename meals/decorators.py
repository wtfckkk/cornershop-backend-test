from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from backend_test.settings import LOGIN_URL


def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=LOGIN_URL,
        redirect_field_name=REDIRECT_FIELD_NAME
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
