from flask import render_template, request, session, redirect, url_for
from klj_site.middleware.auth import require_admin


def register_admin_routes(app):
    @app.route("/adminpage", methods=['GET'])
    @require_admin
    def adminpage():
        return render_template("adminpage.html")
