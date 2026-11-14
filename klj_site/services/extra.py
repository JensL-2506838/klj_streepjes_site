from typing import Any
from klj_site.database.DbConnection import DbConnection


def get_user_id(username):
    db = DbConnection()
    for user in db.get_users():
        if user["username"] == username:
            return user["id"]
    return None
