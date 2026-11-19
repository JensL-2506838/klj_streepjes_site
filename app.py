from flask import Flask
from klj_site.routes import register_routes
from klj_site.middleware.alert_handler import alert_handler
import os

app = Flask(__name__, template_folder="klj_site/templates")
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']

# this is for displaying alerts in the users browser
app.context_processor(alert_handler)

# Connect all routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)