from django.contrib.auth.decorators import user_passes_test


def anonymous_required(function=None, redirect_field_name=None,
                       redirect_to='login'):
    """
    Decorator for views that checks that the user is not logged in (anonymous),
    redirecting to the some page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
