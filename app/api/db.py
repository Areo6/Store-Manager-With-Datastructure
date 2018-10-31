import os
import psycopg2
import psycopg2.extras as ex
from pprint import pprint
from urllib.parse import urlparse


class Database():
    """
    This class creates the database
    """
    def __init__(self):
        """
        This method initializes the database connection and cursor to execute SQL statements
        """
        if os.getenv('APP_SETTINGS') == 'test_db':
            self.db = 'test_db'
        else:
            self.db = 'storemanager'
        try:
            print(self.db)
            print(os.getenv('APP_SETTINGS'))
            self.conn = psycopg2.connect(dbname=self.db, user='postgres', host = 'localhost', password='postgres', port=5432)
            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=ex.RealDictCursor)
        except:
            pprint("Database error")
    
    def create_tables(self):
        """
        This method populates the database with tables
        """
        pprint("Database connected")
        commands = (
            """CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(30) NOT NULL,
                email VARCHAR(30) NOT NULL,
                password VARCHAR(30) NOT NULL,
                user_role VARCHAR(10) NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS products(
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(20) NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                min_qty_allowed INTEGER NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS categories(
                category_id SERIAL PRIMARY KEY,
                category VARCHAR(20) NOT NULL,
                product_id SMALLINT NOT NULL,
                FOREIGN KEY (product_id)
                REFERENCES products (product_id)
                ON UPDATE CASCADE ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS sales(
                sale_id SERIAL PRIMARY KEY,
                product_id SMALLINT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_amount INTEGER NOT NULL,
                attendant_name VARCHAR(30) NOT NULL,
                FOREIGN KEY (sale_id)
                REFERENCES products (product_id)
                ON UPDATE CASCADE ON DELETE CASCADE
            )"""
        )
        for command in commands:
            try:
                self.cur.execute(command)
            except(Exception, psycopg2.DatabaseError) as error:
                pprint(error)
