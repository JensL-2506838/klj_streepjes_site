from flask import render_template, request, session, redirect, url_for
from klj_site.services.auth import is_valid_user
from klj_site.database.DbConnection import DbConnection


def register_login_routes(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("login.html")

        if is_valid_user(request.form.get("username"), request.form.get("password")):
            session['username'], session["password"] = request.form.get("username"), request.form.get("password")
            session['rights'] = db.get_rights(session['username'])
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))
