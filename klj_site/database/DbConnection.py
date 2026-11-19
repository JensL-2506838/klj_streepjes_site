import os
import pymysql
import pymysql.cursors


class QueryExecutor:
    def _get_db(self):
        return pymysql.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            database=os.environ["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def _query(self, sql, params=()):
        db = self._get_db()
        try:
            with db.cursor() as cur:
                cur.execute(sql, params)
                return list(cur.fetchall())
        finally:
            db.close()


class DbConnection(QueryExecutor):
    def get_users(self):
        return self._query("SELECT id, username FROM users")

    def get_requested_users(self):
        return self._query("SELECT id, username FROM requested_users")

    def get_user_id(self, username):
        rows = self._query(
            "SELECT id FROM users WHERE username = %s LIMIT 1",
            (username,),
        )
        return rows[0]["id"] if rows else None

    def get_password_hash(self, user_id):
        rows = self._query(
            "SELECT password_hash FROM users WHERE id = %s LIMIT 1",
            (user_id,),
        )
        return rows[0]["password_hash"] if rows else None

    def get_rights(self, username):
        user_id = self.get_user_id(username)
        rows = self._query(
            "SELECT rights FROM users WHERE id = %s LIMIT 1",
            (user_id,),
        )
        return rows[0]["rights"] if rows else None

    def request_account(self, username, password_hash):
        self._query(
            "INSERT INTO requested_users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )

    def approve_user(self, request_id):
        # request_id is the id of the row in requested_users (not the id in users)
        # 1. Copy the user from requested_users into users (with default 'user' rights)
        self._query(
            """
            INSERT INTO users (username, password_hash, rights)
            SELECT username, password_hash, 'user'
            FROM requested_users
            WHERE id = %s
            """,
            (request_id,)
        )

        # 2. Remove them from requested_users
        self._query(
            "DELETE FROM requested_users WHERE id = %s",
            (request_id,)
        )

    def decline_user(self, request_id):
        # request_id is the id of the row in requested_users
        self._query(
            "DELETE FROM requested_users WHERE id = %s",
            (request_id,)
        )

    def remove_user(self, user_id):
        self._query(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

    def getPrice(self, name):
        awnser = self._query(
            "SELECT price FROM prices WHERE name = %s",
            (name,)
        )
        return awnser[0]["price"] if awnser else None

    def new_event(self, name, price):
        self._query(
            "INSERT INTO events (name, price) VALUES (%s, %s)",
            (name, price,)
        )

    def get_events(self):
        rows = self._query("SELECT * FROM events")
        return rows if rows else []

    def get_event_price(self, event_id):
        awnser = self._query(
            "SELECT price FROM events WHERE id = %s",
            (event_id,)
        )
        return awnser[0]["price"] if awnser else None

    def get_event_name(self, event_id):
        # needed because routes now only get the id, but the page still shows the name
        awnser = self._query(
            "SELECT name FROM events WHERE id = %s",
            (event_id,)
        )
        return awnser[0]["name"] if awnser else None

    def get_event_id(self, event_name):
        awnser = self._query(
            "SELECT id FROM events WHERE name = %s",
            (event_name,)
        )
        return awnser[0]["id"] if awnser else None

    def delete_event(self, event_id):
        self._query("DELETE FROM events WHERE id = %s", (event_id,))

    def add_participant(self, event_id, user_id):
        # add the participant
        self._query(
            "INSERT INTO event_participants (event_id, user_id) VALUES (%s, %s)",
            (event_id, user_id,)
        )
        # set its drinks to zero
        self._query(
            "INSERT INTO participant_drinks (event_id, user_id, amount) VALUES (%s, %s, 0)",
            (event_id, user_id)
        )

    def get_participants(self, event_id):
        awnser = self._query(
            """SELECT username, id FROM users
               WHERE id in (
                    SELECT user_id FROM event_participants WHERE event_id = %s
               )
            """,
            (event_id,)
        )
        return awnser if awnser else []

    def is_participant(self, event_id, user_id):
        awnser = self._query(
            "SELECT * FROM event_participants WHERE event_id = %s AND user_id = %s",
            (event_id, user_id)
        )
        return True if awnser else False

    def get_amount_of_drinks(self, event_id, user_id):
        awnser = self._query(
            "SELECT amount FROM participant_drinks WHERE event_id = %s AND user_id = %s",
            (event_id, user_id)
        )
        return int(awnser[0]["amount"]) if awnser else 0

    def set_amount_of_drinks(self, event_id, user_id, amount):
        self._query(
            """
            UPDATE participant_drinks
            SET amount = %s
            WHERE event_id = %s AND user_id = %s
            """,
            (amount, event_id, user_id)
        )
