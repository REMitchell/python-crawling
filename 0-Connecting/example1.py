from urllib.request import urlopen

html = urlopen("https://oreilly.com")
print(html.read())
