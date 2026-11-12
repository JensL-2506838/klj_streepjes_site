from flask import render_template, request, session, redirect, url_for


def register_login_routes(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")

        # TODO: check if user is valid trough database
        if request.form.get('username') and request.form.get('password'): # will get replaced with the todo
            session['username'], session["password"] = request.form.get("username"), request.form.get("password")
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))
