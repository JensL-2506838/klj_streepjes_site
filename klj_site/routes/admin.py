from flask import render_template
from klj_site.middleware.auth import require_admin
from klj_site.database.DbConnection import DbConnection

def register_admin_routes(app):
    @app.route("/adminpage")
    @require_admin
    def adminpage():
        db = DbConnection()
        users = db.get_users()
        return render_template("adminpage.html", users=users)