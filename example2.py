from urllib.request import urlopen
from urllib.error import HTTPError
try:
	html = urlopen("https://canvas.harvard.edu/courses/4301")
except HTTPError as e:
	print(e)
else:
	print("It Worked!")