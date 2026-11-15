from klj_site.middleware.auth import require_login
from klj_site.database.DbConnection import DbConnection
from flask import render_template


def register_home_routes(app):
    @app.route("/")
    @require_login
    def dashboard():
        db = DbConnection()
        events = db.get_events()
        return render_template("dashboard.html", events=events)
