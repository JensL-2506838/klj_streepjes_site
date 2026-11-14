from klj_site.middleware.auth import require_login
from flask import render_template


def register_home_routes(app):
    @app.route("/")
    @require_login
    def dashboard():
        return render_template("dashboard.html")
