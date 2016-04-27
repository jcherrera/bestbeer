temp="$1"
search=${temp/ /+}
url="http://beersmithrecipes.com/searchrecipe?uid=&term=$search" 
(wget $url -q -O -) > beerSmithRecipesHTML.txt
python webScrape.py | grep viewrecipe > recipeUrls.txt

