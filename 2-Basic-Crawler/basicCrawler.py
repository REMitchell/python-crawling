from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

##################
# This crawler gets the most recent "Technology" articles
# from Reuters, and prints out their title and lede
# (or the first paragraph)
#################
def getArticle(url):
	print("URL: "+url)
	html = urlopen(url)
	articleObj = BeautifulSoup(html.read(), "lxml")
	#Get article title. This should have a class name ending in "title"
	title = articleObj.find("h1").get_text()
	time = articleObj.find("span",{"class":"timestamp"}).get_text()
	location = ""
	if articleObj.find("span",{"class":"articleLocation"}):
		location = articleObj.find("span",{"class":"articleLocation"}).get_text()
	#Get the main body of the article text
	body = articleObj.find("span", {"id":"article-text"}).get_text()

	print("TITLE: "+title)

	print("AUTHOR: "+time)

	print("LOCATION: "+location)
	print("BODY: "+body)
	print("-----------------------------")

for i in range(0, 10):
	print("Scraping page: "+str(i)+" of articles")
	url = "http://www.reuters.com/news/archive/technologyNews?view=page&page="+str(i)+"&pageSize=10"
	html = urlopen(url)
	listingObj = BeautifulSoup(html.read(), "lxml")
	urls = listingObj.findAll("h3", {"class":"story-title"})
	for url in urls:
		newPage = url.find("a").attrs['href']
		#Ignore external URLs
		if newPage.startswith("/"):
			getArticle("http://reuters.com"+newPage)