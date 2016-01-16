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
		conn.close()

	#########
	# Prints and stores content if content does not already exist for that URL and topic
	#########
	def storeContent(self, topic, site, title, body, url):
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
				cur.execute("INSERT INTO content (topicId, siteId, title, body, url) VALUES(%s, %s, %s, %s, %s)", (int(topic.id), int(site.id), title, body, url))
			except:
				print("Could not store article")
			try:
				conn.commit()
			except:
				conn.rollback()


	def getSites(self):
		global conn
		global cur
		cur.execute("SELECT * FROM sites")
		sitesData = cur.fetchall()
		allSiteObjs = []
		for site in sitesData:
			siteObj = Website(site['id'], site['name'], site['url'], site['searchUrl'], site['resultListing'], site['resultUrl'], site['absoluteUrl'], site['pageTitle'], site['pageBody'])
			allSiteObjs.append(siteObj)
		return allSiteObjs

	def getTopics(self):
		global conn
		global cur
		cur.execute("SELECT * FROM topics")
		topicsData = cur.fetchall()
		allTopicObjs = []
		for topic in topicsData:
			topicObj = Topic(topic['id'], topic['name'])
			allTopicObjs.append(topicObj)
		return allTopicObjs


	################
	# Utilty function used to get a Beautiful Soup object
	# from a given URL
	##############
	def getPage(self, url):
		print("Retrieving URL:\n"+url)
		session = requests.Session()
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
		try:
			req = session.get(url, headers=headers)
		except requests.exceptions.RequestException:
			return None
		bsObj = BeautifulSoup(req.text, "lxml")
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
				
			if pageObj == None:
				print("Something is wrong with that page or URL. Skipping")
			else:
				title = self.safeGet(pageObj, site.pageTitle)
				print("Title is "+title)
				body = self.safeGet(pageObj, site.pageBody)
				if title != "" and body != "":
					self.storeContent(topic, site, title, body, url)


#####################################################
##### "User" code, outside the scraper class ########
#####################################################

crawler = Crawler()
crawler.openCon()
#build a list of websites to search, from the CSV file
sites = crawler.getSites()
topics = crawler.getTopics()

for topic in topics:
	print("GETTING INFO ABOUT: "+topic.name);
	for targetSite in sites:
		print("FROM SITE: "+targetSite.name);
		crawler.search(topic, targetSite)

crawler.closeCon()



