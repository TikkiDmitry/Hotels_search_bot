import psycopg2
from psycopg2 import sql


class DataBase:
    def __init__(self, db_url_object):
        self.conn = psycopg2.connect(db_url_object)
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS history (
                id SERIAL PRIMARY KEY,
                command varchar(15),
                date varchar(100),
                hotels varchar(350)
            )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert(self, command, date, hotels):
        insert_query = sql.SQL("INSERT INTO history (command, date, hotels) VALUES (%s, %s, %s)")
        self.cursor.execute(insert_query, (command, date, hotels))
        self.conn.commit()

    def select(self):
        select_query = sql.SQL("SELECT id, command, date, hotels FROM history")
        self.cursor.execute(select_query)
        return self.cursor.fetchall()