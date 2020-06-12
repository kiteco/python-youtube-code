from bs4 import BeautifulSoup
import urllib.request
import requests

# setting URL destination
url = "https://www.reddit.com/r/BabyYoda"

# retrieving HTML payload from the website
response = requests.get(url)

# checking response.status_code (if you get 502, try rerunning the code)
if response.status_code != 200:
    print(f"Status: {response.status_code} — Try rerunning the code\n")
else:
    print(f"Status: {response.status_code}\n")

# using BeautifulSoup to parse the response object
soup = BeautifulSoup(response.content, "html.parser")

# finding Post images in the soup
images = soup.find_all("img", attrs={"alt":"Post image"})

# downloading images
number = 0
for image in images:
    print(image["src"])
    image_src = image["src"]
    urllib.request.urlretrieve(image_src, str(number))
    number += 1
