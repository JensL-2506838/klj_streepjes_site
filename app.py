from flask import Flask
from site.routes import register_routes

app = Flask(__name__, template_folder="site/templates")
app.secret_key = b"your_secret_key_here"

# Connect all routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)