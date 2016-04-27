from bs4 import BeautifulSoup
soup = BeautifulSoup(open("beerSmithRecipesHTML.txt"))
for link in soup.find_all('a'):
	print(link.get('href')) 
