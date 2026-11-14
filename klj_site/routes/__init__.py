from klj_site.routes.homepage import register_home_routes
from klj_site.routes.login import register_login_routes
from klj_site.routes.admin import register_admin_routes


def register_routes(app):
    register_home_routes(app)
    register_login_routes(app)
    register_admin_routes(app)
