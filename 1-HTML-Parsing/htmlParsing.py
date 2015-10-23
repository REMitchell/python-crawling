from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.oreilly.com/")
bsObj = BeautifulSoup(html)
image = bsObj.find("img", {"alt":"O'Reilly Media, Inc."})
print(image.attrs['src'])