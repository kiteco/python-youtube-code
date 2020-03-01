from bs4 import BeautifulSoup
import urllib.request
import requests

url = "http://www.reddit.com/r/BabyYoda"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
images = soup.find_all("img", attrs={"alt":"Post image"})
number = 0
for image in images:
	print(image["src"])
	image_src = image["src"]
	urllib.request.urlretrieve(image_src, str(number))
	number += 1
