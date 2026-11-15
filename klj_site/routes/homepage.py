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

    @app.route("/event/<string:event_name>")
    @require_login
    def event_visitor(event_name):
        db = DbConnection()
        event_price = db.get_event_price(event_name)
        return render_template(
            "eventPage.html",
            event_name=event_name,
            event_price=event_price
        )
