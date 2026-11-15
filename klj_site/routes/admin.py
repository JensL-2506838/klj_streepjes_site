from flask import render_template, jsonify, request
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

        # TODO: add form post method in here
        return render_template("newEvent.html", standardPrice=5)
