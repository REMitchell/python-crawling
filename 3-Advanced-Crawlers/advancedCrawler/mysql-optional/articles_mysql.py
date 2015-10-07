from website import Website
from topic import Topic
from content import Content

import pymysql
import requests
from bs4 import BeautifulSoup
import sys
from io import StringIO
import csv

class Scraper:
	conn = None
	cur = None

	def __init__(self):
		global conn
		global curcomp
		

	#########
	# Open a MySQL connection. Should be triggered by the caller before running
	# the scraper, if the caller is using MySQL
	#########
	def openCon(self):
		global conn
		global cur
		#Use this line connecting to MySQL on Linux/Unix/MacOSX
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='mysql', charset='utf8')
		#Use this line connecting to MySQL on Windows
		#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd=None, db='mysql' charset='utf8')

		cur = conn.cursor(pymysql.cursors.DictCursor)
		cur.execute("USE articleCrawler")

	#########
	# Close a MySQL connection. Should be triggered by the caller after running
	# the scraper, if the caller is using MySQL
	#########
	def closeCon(self):
		global conn
		global cur
		#conn.close()

	#########
	# Prints and stores content if content does not already exist for that URL and topic
	#########
	def storeContent(self, topic, title, body, url):
		global conn
		global cur
		#Optionally, comment out the print statements if you want this to go straight to
		#MySQL without printing
		print("New article found for: "+topic.name)
		print(title)
		print(body)

		if(len(body) > 9999):
			body = body[:9999]
		if(len(title) > 999):
			title = title[:999]
		cur.execute("SELECT * FROM content WHERE url = %s AND topicId = %s", (url, int(topic.id)))
		if cur.rowcount == 0:
			try:
				cur.execute("INSERT INTO content (topicId, title, body, url) VALUES(%s, %s, %s, %s)", (int(topic.id), title, body, url))
			except:
				print("Could not store article")
			try:
				conn.commit()
			except:
				conn.rollback()

	#########
	# Creates a new topic in the database, if one does not exist. Returns a topic object
	#
	##########
	def getTopicFromName(self, topicName):
		global conn
		global cur
		
		if topicName is None:
			return None
		print("SELECT * FROM topics WHERE name = %s", (topicName))
		cur.execute("SELECT * FROM topics WHERE name = %s", (topicName))
		if cur.rowcount == 0:
			print("INSERT INTO topics (name) VALUES(%s)", (topicName))
			cur.execute("INSERT INTO topics (name) VALUES(%s)", (topicName))
			conn.commit()
			topicId = cur.lastrowid
		else:
			topicId = cur.fetchone()['id']

		print("Creating topic with id "+str(topicId)+" and name "+str(topicName))
		topic = Topic(topicId, topicName)

		#If not using MySQL, return a dummy topic object. This line should be commented
		#out if you are using MySQL
		#topic = Topic(0, topicName, "")
		return topic

	################
	# Utilty function used to get a Beautiful Soup object
	# from a given URL
	##############
	def getPage(self, url):
		session = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
		req = session.get(url, headers=headers)
		bsObj = BeautifulSoup(req.text)
		return bsObj


   	################
	# Utilty function used to get a string from a Beautiful Soup
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
		print(site.searchUrl+topic.name)
		bsObj = self.getPage(site.searchUrl+topic.name)
		searchResults = bsObj.select(site.resultListing)
		for result in searchResults:
			url = result.select(site.resultUrl)[0].attrs["href"]
			#Check to see whether it's a relative or an absolute URL
			
			if(site.absoluteUrl == "true"):
				pageObj = self.getPage(url)
			else:
				pageObj = self.getPage(site.url+url)
			title = self.safeGet(pageObj, site.pageTitle)
			print("Title is "+title)
			body = self.safeGet(pageObj, site.pageBody)
			if title != "" and body != "":
				self.storeContent(topic, title, body, url)

	################
	# Starts a search of a given website for a given topic
	##############
	def scrape(self, topicStr, targetSite):
		global conn
		global cur
		#If using MySQL, this will get any stored details about the topic
		#If not using MySQL, it will essentially do nothing
		topic = self.getTopicFromName(topicStr)
		self.search(topic, targetSite)

#####################################################
##### "User" code, outside the scraper class ########
#####################################################

#Get topics.txt, throw an error if it is not provided
if len(sys.argv) < 2:
	sys.exit("Must provide a filename to read from")

f = open(sys.argv[1], 'r')
topicName = f.readline().strip()
scraper = Scraper()
scraper.openCon()

#Get a list of sites to search from the sites.csv file
data = open('sites.csv', 'r').read()
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
		scraper.scrape(topicName, targetSite)
	topicName = f.readline().strip()

scraper.closeCon()



