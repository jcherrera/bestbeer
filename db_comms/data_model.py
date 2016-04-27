## @package db_comms.data_model
#  Contains classes to hold data retrieved from the database.
#

## Data representation of entries in the User table
#
class User:
	## The classe constructor.
	#  @param user_tuple The tuple returned from a user database query.
	#  @param account_tuple The tuple returned from a account database query.
	def __init__(self, user_tuple, account_tuple):
		## The unique user id.
		self.id = user_tuple[0]
		## The username of the user.
		self.username = user_tuple[1]
		## The account data object of the user.
		self.account = Account(account_tuple)

## Data representation of entries in the account table.
class Account:
	## The class constructor.
	#  @param account_tuple The tuple returned from a account database query.
	def __init__(self, account_tuple):
		## The unique account id.
		self.id = account_tuple[0]
