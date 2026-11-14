from flask import session, redirect, url_for
from functools import wraps


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


def _require_login():
    if 'username' not in session:
        return redirect(url_for("login"))
    return None
require_login = _als_decorator(_require_login)


@require_login
def _require_admin():
    if 'rights' not in session or session['rights'] != 'admin':
        return redirect(url_for("dashboard"))
    return None
require_admin = _als_decorator(_require_admin)
