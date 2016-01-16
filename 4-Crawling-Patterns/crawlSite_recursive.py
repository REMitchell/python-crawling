from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

pages = set()

def formatUrl(url, root):
    if(url.startswith("/")):
        return root+url
    if(url.startswith("http")):
        return url
    return root+"/"+url

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, root):
    internalLinks = []
    parsed_uri = urlparse(root)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    for link in bsObj.findAll("a"):
        if link.has_attr('href'):
            url = link.attrs['href']
            #Check if URL is internal
            if url is not None and "#" not in url and (url.startswith(domain) or not url.startswith("http")):
                url = formatUrl(url, root)
                if url not in internalLinks:
                    internalLinks.append(url)
    return internalLinks

def getLinks(pageUrl, root):
    global pages
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html, "lxml")
    internalLinks = getInternalLinks(bsObj, root)
    print(internalLinks)
    for link in internalLinks:
        if link not in pages:
            #We have encountered a new page
            print("----------------\n"+link)
            pages.add(link)
            getLinks(link, root)

getLinks("http://pythonscraping.com","http://pythonscraping.com") 