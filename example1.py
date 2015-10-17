from urllib.request import urlopen

html = urlopen("https://canvas.harvard.edu/courses/4301")
print(html.read())
