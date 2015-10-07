from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

##################
# This crawler gets the most recent "Business and Finance" articles
# from the Brookings Institute, and prints out their title and lede
# (or the first paragraph)
#################
def getArticle(url):
	print("URL: "+url)
	html = urlopen(url)
	articleObj = BeautifulSoup(html.read())
	#Get article title. This should have a class name ending in "title"
	title = articleObj.find("h1").get_text()

	#Get the main body of the article text
	body = articleObj.find("div", {"itemprop":"articleBody"})
	lede = body.find("div", {"class":"lede"})
	if not lede:
		#If an official lede does not exist, get the first paragraph
		lede = body.find("p")
	print("TITLE: "+title)
	metadata = articleObj.find("p", {"class":"metadata"})
	spans = metadata.findAll("span")

	print("AUTHOR: "+spans[0].get_text())


	print("LEDE: "+lede.get_text())
	print("-----------------------------")

for i in range(0, 10):
	start = str(i*25+1)
	print("Scraping page: "+str(start)+" of articles")
	url = "http://www.brookings.edu/research/commentary?topic=Business%20and%20Finance&start="+start+"&sort=ContentDate"
	html = urlopen(url)
	listingObj = BeautifulSoup(html.read())
	urls = listingObj.findAll("h3", {"class":"title"})
	for url in urls:
		newPage = url.find("a").attrs['href']
		#Ignore external URLs
		if newPage.startswith("/"):
			getArticle("http://brookings.edu"+newPage)