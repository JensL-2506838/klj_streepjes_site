from klj_site.middleware.auth import require_login
from klj_site.database.DbConnection import DbConnection
from klj_site.services.extra import include_participant_drinks
from flask import render_template, session, redirect, url_for


def register_home_routes(app):
    @app.route("/")
    @require_login
    def dashboard():
        db = DbConnection()
        events = db.get_events()
        return render_template("dashboard.html", events=events)

    @app.route("/event/<string:event_name>")
    @require_login
    def event_visitor(event_name):
        db = DbConnection()
        event_price = db.get_event_price(event_name)
        event_id = db.get_event_id(event_name)
        participants = include_participant_drinks(db.get_participants(event_id), event_id)
        return render_template(
            "eventPage.html",
            event_name=event_name,
            event_price=event_price,
            participants=participants,
            user_is_participant=db.is_participant(event_id, session['id'])
        )

    @app.route("/pay/<float:amount>/<string:event_name>")
    @require_login
    def pay(amount, event_name):
        db = DbConnection()
        messages = session.get("alertMessages", [])
        messages.append(f"Your total is {float(amount) * float(db.get_event_price(event_name))}")
        session['alertMessages'] = messages

        db.set_amount_of_drinks(db.get_event_id(event_name), session['id'], 0)

        return redirect(url_for('event_visitor', event_name=event_name))

    @app.route("/participate/<string:event_name>")
    @require_login
    def participate(event_name):
        db = DbConnection()
        event_id = db.get_event_id(event_name)
        if not db.is_participant(event_id, session['id']):
            db.add_participant(event_id, session['id'])
        return redirect(url_for("event_visitor", event_name=event_name))

    @app.route("/increase_drink_counter/<string:event_name>/<int:user_id>")
    @require_login
    def increase_drink_counter(event_name, user_id):
        db = DbConnection()
        event_id = db.get_event_id(event_name)
        cur_amount_of_drinks = db.get_amount_of_drinks(event_id, user_id)
        db.set_amount_of_drinks(event_id, user_id, cur_amount_of_drinks + 1)

        return redirect(url_for("event_visitor", event_name=event_name))

    @app.route("/decrease_drink_counter/<string:event_name>/<int:user_id>")
    @require_login
    def decrease_drink_counter(event_name, user_id):
        db = DbConnection()
        event_id = db.get_event_id(event_name)
        cur_amount_of_drinks = db.get_amount_of_drinks(event_id, user_id)
        if cur_amount_of_drinks > 0:
            db.set_amount_of_drinks(event_id, user_id, cur_amount_of_drinks - 1)

        return redirect(url_for("event_visitor", event_name=event_name))