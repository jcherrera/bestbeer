from comms import *


session = UserSession()

while session.user == None:
	option = input("-  Welcome to the BetterBeer DB Test!\n-  (1)Login\n-  (2)Signup\n>> ")


	if option == 1:
		print "\n-  Login  -"
		username = raw_input("username: ")
		password = raw_input("password: ")
		session.connect_to_db()
		session.login_user(username, password)

	elif option == 2:
		print "\n-  Sign up  -"
		username = raw_input("username: ")
		password = raw_input("password: ")
		session.connect_to_db()
		session.sign_up_user(username, password)

print "Successfully logged in!!"


