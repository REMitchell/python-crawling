from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.oreilly.com/")
bsObj = BeautifulSoup(html)
menuList = bsObj.findAll("li", {"role":"menuitem"})

for item in menuList:
    print(item.get_text())