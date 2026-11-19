from flask import render_template, jsonify, request, redirect, url_for, session
from klj_site.middleware.auth import require_admin
from klj_site.database.DbConnection import DbConnection


def register_admin_routes(app):
    @app.route("/adminpage")
    @require_admin
    def adminpage():
        db = DbConnection()
        users = db.get_users()
        requested_users = db.get_requested_users()
        events = db.get_events()
        return render_template(
            "adminpage.html",
            users=users,
            requested_users=requested_users,
            events=events
        )

    @app.route("/approve_user/<string:username>", methods=["POST"])
    @require_admin
    def approve_user(username):
        db = DbConnection()
        db.approve_user(username)
        return jsonify({"status": "ok"}), 200

    @app.route("/decline_user/<string:username>", methods=["POST"])
    @require_admin
    def decline_user(username):
        db = DbConnection()
        db.decline_user(username)
        return jsonify({"status": "ok"}), 200

    @app.route("/remove_user/<string:username>", methods=['POST'])
    @require_admin
    def remove_user(username):
        db = DbConnection()
        db.remove_user(username)
        return jsonify({"status": "ok"}), 200

    @app.route("/newEvent", methods=['GET', 'POST'])
    @require_admin
    def newEvent():
        db = DbConnection()
        if request.method == 'GET':
            return render_template("newEvent.html", standardPrice=db.getPrice("standardPrice"))

        event_name = request.form.get("title")
        event_price = request.form.get("price")

        # TODO: this will be replaced when every url uses id instead of name
        if any(char in str(event_name) for char in "/+"):
            messages = session.get("alertMessages", [])
            messages.append("Your event title contains invalid characters")
            session['alertMessages'] = messages

            return redirect(url_for("newEvent"))

        if event_name and event_price and float(event_price) >= 0:
            db.new_event(event_name, event_price)
            return redirect(url_for("adminpage"))
        return redirect(url_for("newEvent"))

    @app.route("/deleteEvent/<int:event_id>")
    @require_admin
    def deleteEvent(event_id):
        DbConnection().delete_event(event_id)
        return redirect(url_for('adminpage'))
