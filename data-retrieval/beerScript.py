import argparse
from bs4 import BeautifulSoup
import urllib2
import re
import sys



#Extracts the name of the beer from an appropriate beersmith recipe url.
def url_to_beer_name(url):
	parsed_url= url.split('/')
	return parsed_url[-1].replace('-', ' ').title()

#Finds the search term specified after the executable and stores it in the variablesearch.
parser = argparse.ArgumentParser(description = "Process Search Term")
parser.add_argument('searchTerm')
args = parser.parse_args()
search = args.searchTerm

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
	print "No results,try again."
	sys.exit()

#Prompts the user to pick one of the beers that appeared from the search
print 'Which beer recipe do you want to choose? Type in the appropriate number, from 1 to ' + str(len(links))
iterator=1
parser = []
for link in links:
	print str(iterator)+ ': ' + url_to_beer_name(link)	
	iterator+=1

#Loops until an appropriate response to the promt is given
while(True):
	response = input()
	if isinstance(response, int) and response>=1 and response<=len(links):
		search = links[response-1]
		break
	else:
		print "Invalid response, try again."

#Extracts the html of the chosen beer url are stores it into html.
html = urllib2.urlopen(search)
soup = BeautifulSoup(html.read())
beer_name = url_to_beer_name(search)
print '\n' + beer_name + '\n'


#Finds the Bitterness and ABV values for the appropriate beer and prints it out
trs = soup.find_all('tr')
BittInd = 0;
ABVInd = 0;
for i in range(0,(len(trs)-1)):
	if 'Bitterness' in str(trs[i]):
		BittInd = i
	if 'ABV:' in str(trs[i]):
		ABVInd = i;
temp = str(trs[BittInd].find_all('td')[0])
BittInd= float(re.search(r'\d+\.\d',temp).group())
temp = str(trs[ABVInd].find_all('td')[0])
ABVInd = float(re.search(r'\d+\.\d',temp).group())


#Find a similar beer
beerinfile = 0;
totalDiff = 100000;
suggestion = '';
searchFile = open('beer-data-for-predictions.txt','r+')
for line in searchFile:
	if(~(beer_name in line)):
		searchFile.write(str(beer_name)+","+str(BittInd)+","+str(ABVInd))
	print line
	index = line.index(',')
	abvtemp=float(line[index+6:])
	ibutemp=float(line[index+1, index+4])
	diff = abs(10*(ABVInd-abvtemp)+(BittInd-abvtemp))
	if(diff<totalDiff):
		suggestion = line[:index]
		totalDiff = diff	 

#Print out
print "Bitterness: " + str(BittInd) + ", ABV: " + str(ABVInd)
print suggestion

