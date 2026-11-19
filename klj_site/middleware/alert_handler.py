from flask import session

def add_alert(message):
    """Queue a message that is shown as an alert on the next page that displays alerts."""
    messages = session.get('alertMessages', [])
    messages.append(message)
    session['alertMessages'] = messages


def alert_handler():
    messages = session.get('alertMessages', [])

    session['alertMessages'] = []

    return dict(alertMessages=messages)