import psycopg2
import data_objects as do


class DatabaseAccess:
    def __init__(self, user: str, password: str, host="localhost"):
        self._parameters = {
            'host': host,
            'database': 'properties',
            'user': user,
            'password': password
        }

    def _execute(self, sql, data):
        with psycopg2.connect(**self._parameters) as conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            res = cur.fetchall()
            cur.close()
            conn.commit()
            return res

    def _table_exists(self, table_name: str):
        pass

    @staticmethod
    def _obj_to_list(obj):
        return obj.__dict__.values()

    def insert_user(self, user: do.User):
        sql = 'INSERT INTO users VALUES(%s) RETURNING user_id'
        data = self._obj_to_list(user)
        return self._execute(sql, data)

    def update_user(self, user_id: int, user: do.User):
        sql = 'UPDATE users VALUES(%s) WHERE user_id = %s'
        data = self._obj_to_list(user)
        data.append(user_id)
        return self._execute(sql, data)

    def get_user(self, user_id: int):
        sql = 'SELECT * FROM users WHERE user_id = %s'
        return self._execute(sql, (user_id,))

    def delete_user(self, user_id: int):
        sql = 'DELETE FROM users WHERE user_id = %s'
        return self._execute(sql, (user_id,))

    def create_tables(self):
        commands = (
            '''
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY, 
                user_name VARCHAR(255) NOT NULL,
                user_email VARCHAR(255) NOT NULL,
                user_passwd VARCHAR(255) NOT NULL,
                user_score INTEGER NOT NULL,
                user_down INTEGER
            )
            ''',
            '''
            CREATE TABLE properties (
                property_id SERIAL PRIMARY KEY,
                property_address VARCHAR(255) NOT NULL
            )
            ''',
            '''
            CREATE TABLE units (
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
            CREATE TABLE listings (
                property_id INTEGER PRIMARY KEY,
                listing_status INTEGER NOT NULL,
                listing_price REAL NOT NULL,
                FOREIGN KEY (property_id)
                REFERENCES properties (property_id)
                ON UPDATE CASCADE ON DELETE CASCADE                
            )
            ''',
            '''
            CREATE TABLE user_properties (
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
