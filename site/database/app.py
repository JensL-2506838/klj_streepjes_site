import os
import pymysql
from flask import Flask, jsonify, request, redirect

# Serve the UI folder as static files (HTML, CSS, JS)
app = Flask(__name__, static_folder="../UI", static_url_path="/")


def get_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def query(sql, params=()):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        db.close()


@app.route("/")
def home():
    return redirect("/HTML/index.html")


@app.get("/api/test")
def send_test_message():
    return jsonify({"message": "this is a test message", "status": 200})


@app.get("/api/users")
def get_users():
    return jsonify(query_users())


@app.get("/api/isLoginValid")
def isLoginValid():
    # get submitted username from frontend
    submitted_username = request.args.get("username")

    if not submitted_username:
        return jsonify({"error": "Username not received", "status": 400})

    valid_users = query_users()

    # checking if the submitted username is valid and returning
    for user in valid_users:
        if user["username"] == submitted_username:
            return jsonify({"valid": True, "status": 200})

    return jsonify({"valid": False, "status": 200})


def query_users():
    return query("SELECT username FROM users")
