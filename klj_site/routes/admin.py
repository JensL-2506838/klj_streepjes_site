from flask import render_template, jsonify, request, redirect, url_for
from klj_site.middleware.auth import require_admin
from klj_site.database.DbConnection import DbConnection

def register_admin_routes(app):
    @app.route("/adminpage")
    @require_admin
    def adminpage():
        db = DbConnection()
        users = db.get_users()
        requested_users = db.get_requested_users()
        return render_template("adminpage.html", users=users, requested_users=requested_users)

    @app.route("/approve_user/<string:username>", methods=["POST"])
    @require_admin
    def approve_user(username):
        db = DbConnection()
        db.approve_user(username)  # Runs your Python function
        return jsonify({"status": "ok"}), 200

    @app.route("/newEvent", methods=['GET', 'POST'])
    @require_admin
    def newEvent():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("newEvent.html", standardPrice=db.getPrice("standardPrice"))

        event_name = request.form.get("title")
        event_price = request.form.get("price")
        if event_name and event_price:
            db.new_event(event_name, event_price)
            return redirect(url_for("adminpage"))
        return redirect(url_for("newEvent"))
