## @package db_comms.comms
#  Methods for communicating with postgresql database.
#
import os
import psycopg2
import urlparse
from random import randint
from settings_local import *
from data_model import *
from logging import *

## Session of logged in user
#
#  A new instance of this class is created every time the program is run.
#  It contains information about the logged in user and methods to interact with
#  the online database.
class UserSession:
	## Init method
    def __init__(self):
		## Active user
        self.user = None
		## psycog2 connection
        self.active_conn = None
		## logger for logging queries and errors
        self.logger = Logger(LOG_FILENAME)

	## Connects to online postgres database and inits the active_conn class variable
	#  @param self The object pointer.
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
        
    ## Inserts row into a table in the database.
	#  @param self The object pointer
	#  @param table The name of the table being inserted into
	#  @param *attributes The list of attributes in the new entry
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
    
	## Generates a unique id that does not exist yet in a table.
	#  @param self The object pointer.
	#  @param table The name of the table.
    def generate_new_id(self, table):
        cur = self.active_conn.cursor()
    
        id_in_table = True
        while id_in_table:
            object_id = randint(0, 9999)
    
            if not(self.fetch_id(table, object_id)):
                id_in_table = False
    
        return object_id

	## Fetches the tuple from a table with the requested id.
	#  @param self The object pointer.
	#  @param table The name of the table.
	#  @param object_id The id of the entry we wish to retrieve
    def fetch_id(self, table, object_id):
        cur = self.active_conn.cursor()

        table_id_query = """SELECT DISTINCT id FROM {} WHERE id={}""".format(table, object_id)
        self.logger.log_command(table_id_query)
        cur.execute(table_id_query)
        self.logger.log_completion(None)
        
        result = cur.fetchone()

        return result
        
    ## Signs up new user and sets the user class variable.
	#  The function first checks to make sure the username is not taken. If it's free, then
	#  the user is added to the database and can now log in.
	#  @param self The object pointer.
	#  @param username The username requested by the user.
	#  @param password The password requested by the user.
    def sign_up_user(self, username, password):
    
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

	## Logs in a user that previouslt signed up and sets the user class variable.
	#  First checks that the username exists. If it does then checks if the password matches.
	#  Once both are verified user variable is set.
	#  @param self The object pointer.
	#  @param username The username supplied by the user.
	#  @param password The password supplied by the user.
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

	## Gets the rating the user gave to a beer.
	#  Queries the ratings table of the database looking for entries that match the user id of
	#  the current session and the beer name. Returns a integer from 0-10 or None if no
	#  rating is found.
	#  @param self The object pointer.
	#  @param beer_name The name of the beer that was possibly rated.
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

	## Stores a new rating entry in database
	#  @param self The object pointer.
	#  @param rating The rating value int up to 10.
    def rate_beer(self, beer_name, rating):
        
        self.insert_row("ratings", beer_name, rating, self.user.id)

        return

	## Fetches a list of ratings from the database that have a rating better than 6.
	#  @param self The object pointer.
    def get_favorites(self):

        cur = self.active_conn.cursor()
        query = """SELECT * FROM ratings WHERE user_id={} AND rating > 6 """.format(self.user.id)

        self.logger.log_command(query)
        cur.execute(query)
        self.logger.log_completion(None)

        favorites = cur.fetchall()

        return favorites

    ## Logs out user.
    def log_out(self):
        self.user = None


