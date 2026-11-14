from flask import render_template
from klj_site.middleware.auth import require_admin


def register_admin_routes(app):
    @app.route("/adminpage")
    @require_admin
    def adminpage():
        return render_template("adminpage.html")
