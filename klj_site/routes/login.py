from flask import render_template, request, session, redirect, url_for
from klj_site.services.auth import is_valid_user, hash_password
from klj_site.database.DbConnection import DbConnection


def register_login_routes(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("login.html")

        if is_valid_user(request.form.get("username"), request.form.get("password")):
            session['username'], session["password"] = request.form.get("username"), request.form.get("password")
            session['id'] = db.get_user_id(session['username'])
            session['rights'] = db.get_rights(session['username'])
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("register.html")

        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return redirect(url_for("register"))

        db.request_account(username, hash_password(password))

        messages = session.get("alertMessages", [])
        messages.append(
            "Your account has been requested. You must wait for an administrator to accept your request."
        )

        session['alertMessages'] = messages

        return redirect("login")
