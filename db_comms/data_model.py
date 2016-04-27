

class User:
	def __init__(self, user_tuple, account_tuple):
		self.id = user_tuple[0]
		self.username = user_tuple[1]
		self.account = Account(account_tuple)

class Account:
	def __init__(self, account_tuple):
		self.id = account_tuple[0]
