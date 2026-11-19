import pymysql
from flask import render_template, request, session, redirect, url_for
from klj_site.services.auth import is_valid_user, hash_password
from klj_site.database.DbConnection import DbConnection
from klj_site.middleware.alert_handler import add_alert


def register_login_routes(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("login.html")

        try:
            if is_valid_user(request.form.get("username"), request.form.get("password")):
                session['username'], session["password"] = request.form.get("username"), request.form.get("password")
                session['id'] = db.get_user_id(session['username'])
                session['rights'] = db.get_rights(session['username'])
                return redirect(url_for("dashboard"))
        except pymysql.MySQLError:
            app.logger.exception("Database error in login")
            # the session may be half filled in (username set, id missing), so start clean
            session.clear()
            add_alert("Could not log in right now, please try again later.")
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

        try:
            db.request_account(username, hash_password(password))
        except pymysql.IntegrityError:
            # username is UNIQUE in requested_users, so this name was already requested
            messages = session.get("alertMessages", [])
            messages.append("That username has already been requested.")
            session['alertMessages'] = messages
            return redirect(url_for("register"))
        except pymysql.MySQLError:
            app.logger.exception("Database error in register")
            add_alert("Could not request your account, please try again later.")
            return redirect(url_for("register"))

        messages = session.get("alertMessages", [])
        messages.append(
            "Your account has been requested. You must wait for an administrator to accept your request."
        )

        session['alertMessages'] = messages

        return redirect("login")
