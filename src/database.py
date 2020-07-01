import psycopg2
import psycopg2.extras
import data_objects as do
import logging


class DatabaseAccess:
    def __init__(self, user: str, password: str, database="properties",host="localhost"):
        self._parameters = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }

    def _execute(self, sql, data):
        with psycopg2.connect(**self._parameters) as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql, data)
            res = None
            try:
                res = cur.fetchall()
            except psycopg2.ProgrammingError as e:
                logging.warning(e)
            cur.close()
            conn.commit()
            return res

    @staticmethod
    def _obj_to_list(obj):
        return list(obj.__dict__.values())

    @staticmethod
    def _format_values(values_list: list):
        return ''.join(['\'' + str(item) + '\', ' for item in values_list])[:-2]

    def insert_user(self, user: do.User):
        sql = 'INSERT INTO users(user_name, user_email, user_passwd, user_score, user_down) ' \
              'VALUES(%s, %s, %s, %s, %s) RETURNING user_id'
        return self._execute(sql, (user.name, user.email, user.passwd, user.score, user.down))[0]['user_id']

    def update_user(self, user_id: int, user: do.User):
        sql = 'UPDATE users SET (user_name, user_email, user_passwd, user_score, user_down) = ' \
              '(%s, %s, %s, %s, %s) ' \
              'WHERE user_id = %s RETURNING user_id'
        return self._execute(sql, (user.name, user.email, user.passwd, user.score, user.down, user_id))[0]['user_id']

    def find_user(self, user_id: int):
        sql = 'SELECT * FROM users WHERE user_id = %s'
        data = self._execute(sql, (user_id, ))
        user = None
        if len(data) > 0:
            user = do.User(data[0]['user_name'],
                           data[0]['user_email'],
                           data[0]['user_score'],
                           data[0]['user_down'])
            user.passwd = data[0]['user_passwd']
        return user

    def delete_user(self, user_id: int):
        sql = 'DELETE FROM users WHERE user_id = %s'
        return self._execute(sql, (user_id, ))

    def create_tables(self):
        commands = (
            '''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY, 
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                user_passwd BYTEA NOT NULL,
                user_score INTEGER NOT NULL,
                user_down INTEGER
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS properties (
                property_id SERIAL PRIMARY KEY,
                property_address TEXT NOT NULL
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS units (
                property_id INTEGER PRIMARY KEY,
                unit_baths INTEGER NOT NULL,
                unit_bets INTEGER NOT NULL,
                unit_rent INTEGER NOT NULL,
                FOREIGN KEY (property_id)
                REFERENCES properties (property_id)
                ON UPDATE CASCADE ON DELETE CASCADE
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS listings (
                property_id INTEGER PRIMARY KEY,
                listing_status INTEGER NOT NULL,
                listing_price REAL NOT NULL,
                FOREIGN KEY (property_id)
                REFERENCES properties (property_id)
                ON UPDATE CASCADE ON DELETE CASCADE                
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS user_properties (
                user_id INTEGER NOT NULL,
                property_id INTEGER NOT NULL,
                PRIMARY KEY (user_id , property_id),
                FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (property_id)
                    REFERENCES properties (property_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            ''')

        with psycopg2.connect(**self._parameters) as conn:
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
