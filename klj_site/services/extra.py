from klj_site.database.DbConnection import DbConnection


def get_user_id(username):
    db = DbConnection()
    for user in db.get_users():
        if user["username"] == username:
            return user["id"]
    return None

def include_participant_drinks(participants, event_id):
    db = DbConnection()
    result = []
    for participant in participants:
        amount = db.get_amount_of_drinks(event_id, participant['id'])
        result.append({**participant, "amount": amount})
    return result
