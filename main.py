## @package main
#  Programs main function and processes
#
#

from db_comms.comms import *
from data_retrieval.beerScript import *
import time
from logo import logo

## The current user session for the application
session = UserSession()

def valid_input():
	while(True):
		try:
			return int(input(">> "))
		except:
			print ("Invalid input.")

## Run the login or signup process
#
#  Prompts the user with two options, login or sign up. Loops until one of these proccesses is
#  successful and the user is set.
def bb_login():
    while session.user == None:
        print("\n - Welcome to the Better Beer! -\n1: Login\n2: Signup\n3: Exit")
        option = valid_input()
    
    
        if option == 1:
            print "\n-  Login  -"
            username = raw_input("username: ")
            password = raw_input("password: ")
            session.connect_to_db()
            if session.active_conn:
                session.login_user(username, password)
    
        elif option == 2:
            print "\n-  Sign up  -"
            username = raw_input("username: ")
            password = raw_input("password: ")
            session.connect_to_db()
            if session.active_conn:
                session.sign_up_user(username, password)

        else:
            quit()
    
    print "\nHello " + username + "!\n"


## Run the beer search process
#
#  Prompts the user for a search term. Searches for that term and provides user with results.
#  User is then prompted to select from the results. The selected result info and user rating
#  is displayed. If the user has yet to rate the beer in the result then they are prompted to do
#  so. If the rating is high enough a sugesstion for another beer is displayed.
def bb_search():
    search = raw_input("\nsearch: ")
    links = search_for_beer(search)
    
    if(len(links) == 0):
        print "No results"
        return

    #Prompts the user to pick one of the beers that appeared from the search
    print '\nWhich beer recipe do you want to choose? Type in the appropriate number, from 1 to ' + str(len(links))

    iterator=1
    parser = []
    for link in links:
        print str(iterator)+ ': ' + url_to_beer_name(link)
        iterator+=1

    #Loops until an appropriate response to the promt is given
    while(True):
        response = input(">> ")
        if isinstance(response, int) and response>=1 and response<=len(links):
            search = links[response-1]
            break
        else:
            print "Invalid response, try again."

    bittind = display_beer_info(search)

    beer_name = url_to_beer_name(search)

    rating = session.get_beer_rating(beer_name)

    if rating:
        print "Your rating:\t" + str(rating) + " / 10"
    else:
        rate = raw_input("\nWould you like to rate this beer?(y/n)\n>> ")
        if rate == 'y':
            while(True):
                rating = input("\nRating(out of 10): ")
                if isinstance(rating, int) and rating > -1 and rating < 11:
                    session.rate_beer(beer_name, rating)
                    break
                else:
                    print "Invalid response, try again."
            
    if rating > 6:
        suggestion = get_similar_beer(bittind)
        print "\nYou really enjoyed this beer! " + suggestion
                
    raw_input ("\nPress enter to continue...")
        
## Run the show favorites process
#
#  The beers that the user has rated above a 6 are displayed in a lis
def bb_favorites():
    
    ratings = session.get_favorites()
    
    print("\n - Favorite Beers -")

    if(ratings):
        print "Beer\t\tRating"
        for rating in ratings:
            print rating[0] + "\t" + str(rating[1]) + " / 10"
    else:
        print "No beers rated above 6 / 10"

    raw_input ("\nPress enter to continue...")

## Main function of application
#
#
def main():

    print logo

    while(True):
        bb_login()

        time.sleep(2)
    
        while(session.user): 
            print("\n- Menu -\n1: Search for beer\n2: View favorites\n3: Log out")
            option = valid_input()
            if option == 1:
                bb_search()
            elif option == 2:
                bb_favorites()
            else:
                session.log_out()
    
if __name__ == "__main__":
    main()
