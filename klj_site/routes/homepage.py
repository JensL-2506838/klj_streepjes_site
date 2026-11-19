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

    @app.route("/event/<int:event_id>")
    @require_login
    def event_visitor(event_id):
        db = DbConnection()
        # the url only has the id, so look up the name and price for the page
        event_name = db.get_event_name(event_id)
        event_price = db.get_event_price(event_id)
        participants = include_participant_drinks(db.get_participants(event_id), event_id)
        return render_template(
            "eventPage.html",
            event_id=event_id,
            event_name=event_name,
            event_price=event_price,
            participants=participants,
            user_is_participant=db.is_participant(event_id, session['id'])
        )

    @app.route("/pay/<float:amount>/<int:event_id>")
    @require_login
    def pay(amount, event_id):
        db = DbConnection()
        messages = session.get("alertMessages", [])
        messages.append(f"Your total is {float(amount) * float(db.get_event_price(event_id))}")
        session['alertMessages'] = messages

        db.set_amount_of_drinks(event_id, session['id'], 0)

        return redirect(url_for('event_visitor', event_id=event_id))

    @app.route("/participate/<int:event_id>")
    @require_login
    def participate(event_id):
        db = DbConnection()
        if not db.is_participant(event_id, session['id']):
            db.add_participant(event_id, session['id'])
        return redirect(url_for("event_visitor", event_id=event_id))

    @app.route("/increase_drink_counter/<int:event_id>/<int:user_id>")
    @require_login
    def increase_drink_counter(event_id, user_id):
        db = DbConnection()
        cur_amount_of_drinks = db.get_amount_of_drinks(event_id, user_id)
        db.set_amount_of_drinks(event_id, user_id, cur_amount_of_drinks + 1)

        return redirect(url_for("event_visitor", event_id=event_id))

    @app.route("/decrease_drink_counter/<int:event_id>/<int:user_id>")
    @require_login
    def decrease_drink_counter(event_id, user_id):
        db = DbConnection()
        cur_amount_of_drinks = db.get_amount_of_drinks(event_id, user_id)
        if cur_amount_of_drinks > 0:
            db.set_amount_of_drinks(event_id, user_id, cur_amount_of_drinks - 1)

        return redirect(url_for("event_visitor", event_id=event_id))