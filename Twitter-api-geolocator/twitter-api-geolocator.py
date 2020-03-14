from TwitterAPI import TwitterAPI
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import json

consumer_key= ""
consumer_secret= ""
access_token_key= ""
access_token_secret= ""


api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)

response = api.request("statuses/filter", {"track": ["harry", "and", "meghan"]})
tweets = response.get_iterator()

coordinates = []
count = 0

while count < 100:
	tweet = next(tweets)
	if "place" in tweet and tweet["place"] != None:
		location = tweet["place"]["bounding_box"]["coordinates"][0][0]
		coordinates.append(location)
		count += 1

world_map = gpd.read_file("C:/Users/Brian/Desktop/TM_WORLD_BORDERS_SIMPL-0.3/TM_WORLD_BORDERS_SIMPL-0.3.shp")

fig, ax = plt.subplots(figsize = (15, 15))
world_map.plot(ax=ax)

for x, y in coordinates:
	plt.scatter(x, y, marker="o", c="red")

plt.savefig("map.png")

