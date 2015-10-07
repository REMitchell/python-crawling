from website import Website
from topic import Topic
from content import Content

import pymysql
import requests
from bs4 import BeautifulSoup
import sys
from io import StringIO
import csv

class Crawler:
	conn = None
	cur = None

#	def __init__(self):
#		print("Starting!")


	#########
	# Prints content, can be integrated with MySQL to store things
	#########
	def printContent(self, topic, title, body, url):
		print("New article found for: "+topic.name)
		print(title)
		print(body)


	#########
	# Creates a new topic object, from a topic string
	##########
	def getTopicFromName(self, topicName):
		topic = Topic(0, topicName)
		return topic

	################
	# Utilty function used to get a Beautiful Soup object
	# from a given URL
	##############
	def getPage(self, url):
		print("Retrieving URL:\n"+url)
		session = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
		req = session.get(url, headers=headers)
		bsObj = BeautifulSoup(req.text)
		return bsObj


   	################
	# Utilty function used to get a content string from a Beautiful Soup
	# object and a selector. Returns an empty string if no object
	# is found for the given selector
	##############
	def safeGet(self, pageObj, selector):
		childObj = pageObj.select(selector)
		if childObj is not None and len(childObj) > 0:
			return childObj[0].get_text()
		return ""


	################
	# Searches a given website for a given topic and records all 
	# pages found
	##############
	def search(self, topic, site):
		bsObj = self.getPage(site.searchUrl+topic.name)
		searchResults = bsObj.select(site.resultListing)
		for result in searchResults:
			url = result.select(site.resultUrl)[0].attrs["href"]
			#Check to see whether it's a relative or an absolute URL
			
			if(site.absoluteUrl == "TRUE"):
				pageObj = self.getPage(url)
			else:
				pageObj = self.getPage(site.url+url)
			title = self.safeGet(pageObj, site.pageTitle)
			print("Title is "+title)
			body = self.safeGet(pageObj, site.pageBody)
			if title != "" and body != "":
				self.printContent(topic, title, body, url)

	################
	# Starts a search of a given website for a given topic
	##############
	def crawl(self, topicStr, targetSite):
		global conn
		global cur
		#If using MySQL, this will get any stored details about the topic
		#If not using MySQL, it will essentially do nothing
		topic = self.getTopicFromName(topicStr)
		self.search(topic, targetSite)

#####################################################
##### "User" code, outside the scraper class ########
#####################################################

f = open("topics.txt", 'r')
topicName = f.readline().strip()
crawler = Crawler()

#Get a list of sites to search from the sites.csv file
data = open("sites.csv", 'r').read()
dataFile = StringIO(data)
siteRows = csv.reader(dataFile)

#Skip the heder line in the CSV file - the header makes it easy to read,
#but we don't want to use the column titles as actual site data
next(siteRows)

#build a list of websites to search, from the CSV file
sites = []
for row in siteRows:
	sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

while(topicName):
	print("GETTING INFO ABOUT: "+topicName);
	for targetSite in sites:
		crawler.crawl(topicName, targetSite)
	topicName = f.readline().strip()




