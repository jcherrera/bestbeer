import os
import psycopg2
import urlparse
from random import randint
from settings_local import *
from data_model import *
from logging import *

class UserSession:
    def __init__(self):
        self.user = None
        self.active_conn = None
        self.logger = Logger(LOG_FILENAME)

    def connect_to_db(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(DATABASE_URL)
    
        self.logger.log_command("Connecting to database")
        try:
            self.active_conn = psycopg2.connect(database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            self.active_conn.autocommit = True
        except:
            self.logger.log_completion("Failed to connect to database.", print_error=True)
            self.active_conn = None
        else:
            self.logger.log_completion(None)
        
    
    def insert_row(self, table, *attributes):
        insert_statement = """INSERT INTO {} VALUES {};""".format(table, str(attributes))
    
        cur = self.active_conn.cursor()

        self.logger.log_command(insert_statement)
        try:
            cur.execute(insert_statement)
        except:
            self.logger.log_completion("Failed to insert row into {}".format(table))
        else:
            self.logger.log_completion(None)
    
    def generate_new_id(self, table):
        cur = self.active_conn.cursor()
    
        id_in_table = True
        while id_in_table:
            object_id = randint(0, 9999)
    
            if not(self.fetch_id(table, object_id)):
                id_in_table = False
    
        return object_id

    def fetch_id(self, table, object_id):
        cur = self.active_conn.cursor()

        table_id_query = """SELECT DISTINCT id FROM {} WHERE id={}""".format(table, object_id)
        self.logger.log_command(table_id_query)
        cur.execute(table_id_query)
        self.logger.log_completion(None)
        
        result = cur.fetchone()

        return result
        
    
    def sign_up_user(self, username, password):
        if self.active_conn == None:
            connect_to_db()
    
        cur = self.active_conn.cursor()
    
        check_query = """SELECT DISTINCT username FROM users WHERE UPPER(username) LIKE UPPER('%{}%') """.format(username)

        self.logger.log_command(check_query)
        cur.execute(check_query)
        self.logger.log_completion(check_query)
    
        user = cur.fetchone()
        if user != None:
            self.logger.log_completion("Username is taken", print_error=True)
            return 1
    
        user_id = self.generate_new_id("users")
        account_id = self.generate_new_id("accounts")
        self.insert_row("users", user_id, username, password, account_id)
        self.insert_row("accounts", account_id, user_id)

        self.user = User((user_id, username), (account_id,))

        self.logger.log_command("User successfully signed up")
        return 0

    def login_user(self, username, password):

        cur = self.active_conn.cursor()
        check_query = """SELECT DISTINCT * FROM users WHERE UPPER(username) LIKE UPPER('%{}%') """.format(username)

        self.logger.log_command(check_query)
        cur.execute(check_query)
        self.logger.log_completion(None)
        
        user = cur.fetchone()
        if user == None:
            self.logger.log_completion("Username incorrect", print_error=True)
            return 1

        if password != user[2]:
            self.logger.log_completion("Password incorrect", print_error=True)
            return 1

        account_id = user[3]
        account = self.fetch_id("accounts", account_id)

        self.user = User(user, account)

        self.logger.log_command("User successfully logged in")

        return 0

    def get_beer_rating(self, beer_name):
        
        cur = self.active_conn.cursor()
        check_query = """SELECT rating FROM ratings WHERE user_id={} AND UPPER(beer_name) LIKE UPPER('%{}%') """.format(self.user.id, beer_name)

        self.logger.log_command(check_query)
        cur.execute(check_query)
        self.logger.log_completion(None)

        rating = cur.fetchone()

        if rating:
            return rating[0]
        else:
            return None


    def rate_beer(self, beer_name, rating):
        
        self.insert_row("ratings", beer_name, rating, self.user.id)

        return


    def get_favorites(self):

        cur = self.active_conn.cursor()
        query = """SELECT * FROM ratings WHERE user_id={} AND rating > 6 """.format(self.user.id)

        self.logger.log_command(query)
        cur.execute(query)
        self.logger.log_completion(None)

        favorites = cur.fetchall()

        return favorites

