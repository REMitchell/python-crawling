from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import time

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html, "lxml")
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id ="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    links = bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
    randomLink = links[random.randint(0, len(links)-1)]
    while randomLink.attrs['href'] in pages:
        randomLink = links[random.randint(0, len(links)-1)]


    #We have encountered a new page
    newPage = randomLink.attrs['href']
    print("----------------\n"+newPage)
    pages.add(newPage)
    time.sleep(1)
    getLinks(newPage)
getLinks("") 