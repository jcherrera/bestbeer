import argparse
from bs4 import BeautifulSoup
import urllib2
import re
import sys



#Extracts the name of the beer from an appropriate beersmith recipe url.
def url_to_beer_name(url):
	parsed_url= url.split('/')
	return parsed_url[-1].replace('-', ' ').title()

def search_for_beer(search):
	#Converts the search term into the appropriate beersmithrecipes.com url.
	search = search.replace(' ', '+')
	search = "http://beersmithrecipes.com/searchrecipe?uid=&term=" + search

	#Extracts the html from the url stored in search and stores it in the variable html.
	html = urllib2.urlopen(search)

	#uses beautifulsoup to extract all the links from the html and stores them in links if they are a recipe url.
	soup = BeautifulSoup(html.read())
	links = []
	for link in soup.find_all('a'):
		if "viewrecipe" in link.get('href'):
			links.append(link.get('href'))

	#Ends program when no recipe urls are found.
	if len(links)==0:
		print "No results for " + search
		return None
	else:
		return links

def display_beer_info(search):
	#Extracts the html of the chosen beer url are stores it into html.
	html = urllib2.urlopen(search)
	soup = BeautifulSoup(html.read())
	print '\n - ' + url_to_beer_name(search) + ' -\n'

	#Finds the Bitterness and ABV values for the appropriate beer and prints it out
	trs = soup.find_all('tr')
	BittInd = 0;
	ABVInd = 0;
	for i in range(0,(len(trs)-1)):
		if 'Bitterness' in str(trs[i]):
			BittInd = i
		if 'ABV' in str(trs[i]):
			ABVInd = i;

	#Print out
	out = str((trs[BittInd].find_all('td'))[0])+'\n' + str((trs[ABVInd].find_all('td'))[0])
	regex = re.compile('<.{0,4}>')
	print regex.sub('',out)

	return BittInd
	
def get_similar_beer(BittInd):
	#Find a similar beer 
	suggestion = "Unfortunately We could not find another suggested beer for you."
	if BittInd == 22.8:
		suggestion = "You Should try a Heineken"
	
	return suggestion	
