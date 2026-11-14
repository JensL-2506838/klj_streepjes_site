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
