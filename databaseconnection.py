import sqlite3
import os
import json

class ConnectDatabase:


    def __init__(self, sql_query) -> None:
        self.cursor = None
        self.sql_query: str = sql_query
        self.connect_database()


    def connect_database(self):
        try:
            with sqlite3.connect('recipes.sqlite') as self.conn:
                self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)

    def execute_sql_with_values(self, value=None) -> list:
        with self.conn:
            return self.cursor.execute(self.sql_query, value).fetchall()

    def execute_sql_without_values(self,) -> list:
        with self.conn:
            return self.cursor.execute(self.sql_query).fetchall()

    def execute_insert_query(self, value) -> None:
        with self.conn:
            self.cursor.execute(self.sql_query, value)

    def execute_update_query(self, value) -> None:
        with self.conn:
            self.cursor.execute(self.sql_query, value)

    def execute_delete_query(self, value) -> None:
        with self.conn:
            self.cursor.execute(self.sql_query, value)

    def close_connect(self) -> None:
        self.conn.close()



