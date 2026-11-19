from flask import session

def alert_handler():
    messages = session.get('alertMessages', [])

    session['alertMessages'] = []

    return dict(alertMessages=messages)