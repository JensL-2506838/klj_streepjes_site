from flask import session, redirect, url_for
from functools import wraps


def _require_login():
    if 'username' not in session:
        return redirect(url_for("login"))
    return None


def _als_decorator(controle):
    """Turn one of the checks above into a decorator."""
    def decorator(functie):
        @wraps(functie)  # keeps the name of the original function (Flask needs unique names)
        def wrapper(*args, **kwargs):
            weigering = controle()
            if weigering is not None:
                return weigering
            return functie(*args, **kwargs)
        return wrapper
    return decorator

require_login = _als_decorator(_require_login)
