from flask import Flask, jsonify, request
import pymysql
from klj_site.routes import register_routes
from klj_site.middleware.alert_handler import alert_handler
import os

app = Flask(__name__, template_folder="klj_site/templates")
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']

# this is for displaying alerts in the users browser
app.context_processor(alert_handler)

# Connect all routes
register_routes(app)


# Catches every database error that no route handled itself
@app.errorhandler(pymysql.MySQLError)
def handle_db_error(error):
    # the full error goes to the logs, the user only sees a generic message
    app.logger.exception("Database error")

    # these routes are called with a POST and answer in JSON, so error in JSON too
    if request.endpoint in ("approve_user", "decline_user", "remove_user"):
        return jsonify({"status": "error"}), 500
    return "Something went wrong, please try again later.", 500


if __name__ == "__main__":
    app.run(debug=True)