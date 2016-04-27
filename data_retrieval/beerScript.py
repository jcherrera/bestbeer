import argparse
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os



## Extracts the name of the beer from an appropriate beersmith recipe url.
#  @param url Url to be converted.
def url_to_beer_name(url):
	parsed_url= url.split('/')
	return parsed_url[-1].replace('-', ' ').title()

## Opens an html based on search and extracts a list of links.
#  @param search The string to search on.
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

## Extracts the html of the chosen link and diplays its info.
#  @param search The url of the chosen beer.
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
	out = regex.sub('',out)
	print out

	bitterness = float(out[12:16])

	return bitterness
	
## Finds other beer with similar bitternes and returns a string suggesting that beer.
#  @param BittInd The bitterness index to search for.
def get_similar_beer(BittInd):
	#Find a similar beer 
	script_dir = os.path.dirname(__file__)
	rel_path = "beer-data-for-predictions.txt"
	abs_file_path = os.path.join(script_dir, rel_path)
	with open(abs_file_path) as fo:
		beer_name = None
		bi_string = "0.0"
		line2 = "tmp"
		while(not(beer_name) and len(line2) > 0):
			line1 = fo.readline()
			try:
				line2 = fo.readline()
			except:
				break

			if len(line2) > 10 and line2[10] == ':':
				bi_string = line2[12:16]
				if abs(float(bi_string) - BittInd) < 5:
					beer_name = line1
					break

	suggestion = "Unfortunately We could not find another suggested beer for you."
	if beer_name:
		suggestion = "You Should try a " + beer_name
	
	return suggestion	


