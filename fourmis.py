#Imports
from random import uniform
from haversine import haversine
import pants
import csv
import os, sys
import requests
from urllib.parse import quote
import matplotlib.pyplot as plt
import base64
import re

#Constants
CSV_FILENAME = "open_pubs.csv"
#CSV_FILENAME = "london_pubs.csv"
USE_MILES_UNIT = False #if false, will use Kilometers
try:
	GOOGLE_API_TOKEN = os.environ['GOOGLE_API_TOKEN']
except:
	print("You need to define the GOOGLE_API_TOKEN env variable to use GOOGLE GEOLOC API")
	sys.exit(1)

NUMBER_NODES = int(os.getenv('NUMBER_NODES', 0))

MAP_CENTER = os.getenv('MAP_CENTER', False)
MAP_CENTER = MAP_CENTER in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

nodes = []
def calcul_distance(a, b):
	return haversine(a, b, miles=USE_MILES_UNIT)

if not os.path.exists("./data"):
    os.makedirs("./data")

if not os.path.isfile("./data/clean.csv"):
	with open(CSV_FILENAME, 'r') as csvfile:
		print("Starting csv load and cleaning")
		reader = csv.reader(csvfile, doublequote=True, skipinitialspace=True)
		next(reader, None)
		for index, row in enumerate(reader):
			vals = (None, None)
			if row[8] == "":
				with open(CSV_FILENAME, 'r') as secondssvfile:
					for i, line in enumerate(secondssvfile):
						if i == index:
							r = csv.reader([line], doublequote=True, skipinitialspace=True)
							row = next(r)
							break
			# Check if the latitude or longitude is null
			if '\\N' in row[-3:][:2]:
				res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}".format(GOOGLE_API_TOKEN, quote(row[2]))).json()
				if res['status'] != 'OK':
					if res['status'] == 'ZERO_RESULTS':
						print("Can't find the location for {} on ".format(row[2], index))
						print(row)
					else:
						print(res)
				else:
					res = res['results'][0]['geometry']['location']
					vals = (float(res['lat']), float(res['lng']))
					#print(vals)
			else:
				vals = (float(row[6]), float(row[7]))
			if None not in vals:
				nodes.append(vals)
	print("{} nodes found".format(len(nodes)))
	print("Finished csv load")

	nodes = [node for i, node in enumerate(nodes) if NUMBER_NODES <= 0 or i < NUMBER_NODES]
	nodes = list(set(nodes))
	print("{} clean nodes found".format(len(nodes)))
	
	print("Writing temp file")
	with open('data/clean.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
		rows = [list(node) for node in nodes]
		print(rows[0])
		spamwriter.writerows(rows)
	print("Finished writing temp file")
else:
	print("Temp file found, reading it")
	with open('./data/clean.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, doublequote=True, skipinitialspace=True)
		for row in reader:
			vals = (float(row[0]), float(row[1]))
			nodes.append(vals)
	nodes = [node for i, node in enumerate(nodes) if NUMBER_NODES <= 0 or i < NUMBER_NODES]
	print("Temp file load finished")


#Code

print("Creating world")
world = pants.World(nodes, calcul_distance)
print("Finished creating world")

print("Creating solver")
solver = pants.Solver()
print("Finished creating solver")

print("Starting solving world")
solutions = solver.solutions(world)
best = float("inf")
solution = None
for solution in solutions:
	if solution.distance < best:
		best = solution.distance
		solution = solution
print("Finished solving world")

print("the best distance is {} {}".format(round(best, 3), "miles" if USE_MILES_UNIT else "km"))

print("Generating the map")

htmlTemplate = "PCFET0NUWVBFIGh0bWw+DQo8aHRtbD4NCiAgPGhlYWQ+DQogICAgPG1ldGEgbmFtZT0idmlld3BvcnQiIGNvbnRlbnQ9ImluaXRpYWwtc2NhbGU9MS4wLCB1c2VyLXNjYWxhYmxlPW5vIj4NCiAgICA8bWV0YSBjaGFyc2V0PSJ1dGYtOCI+DQogICAgPHRpdGxlPlNpbXBsZSBQb2x5bGluZXM8L3RpdGxlPg0KICAgIDxzdHlsZT4NCiAgICAgICNtYXAgew0KICAgICAgICBoZWlnaHQ6IDEwMCU7DQogICAgICB9DQogICAgICBodG1sLCBib2R5IHsNCiAgICAgICAgaGVpZ2h0OiAxMDAlOw0KICAgICAgICBtYXJnaW46IDA7DQogICAgICAgIHBhZGRpbmc6IDA7DQogICAgICB9DQogICAgPC9zdHlsZT4NCiAgPC9oZWFkPg0KICA8Ym9keT4NCiAgICA8ZGl2IGlkPSJtYXAiPjwvZGl2Pg0KICAgIDxzY3JpcHQ+DQoJdmFyIHZhbHVlcyA9IHt9IDsNCglmdW5jdGlvbiBpbml0TWFwKCkgew0KICAgICAgICB2YXIgbWFwID0gbmV3IGdvb2dsZS5tYXBzLk1hcChkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbWFwJyksIHsNCiAgICAgICAgICB6b29tOiB7fSAsDQogICAgICAgICAgY2VudGVyOiB7bGF0OiB7fSAsIGxuZzoge30gfSwNCiAgICAgICAgICBtYXBUeXBlSWQ6ICd0ZXJyYWluJw0KICAgICAgICB9KTsNCgkJDQoJCXZhciBmbGlnaHRQbGFuQ29vcmRpbmF0ZXMgPSB2YWx1ZXMubWFwKHYgPT4gKHtsYXQ6IHZbMF0sIGxuZzogdlsxXX0pKQ0KICAgICAgICB2YXIgZmxpZ2h0UGF0aCA9IG5ldyBnb29nbGUubWFwcy5Qb2x5bGluZSh7DQogICAgICAgICAgcGF0aDogZmxpZ2h0UGxhbkNvb3JkaW5hdGVzLA0KICAgICAgICAgIGdlb2Rlc2ljOiB0cnVlLA0KICAgICAgICAgIHN0cm9rZUNvbG9yOiAnI0ZGMDAwMCcsDQogICAgICAgICAgc3Ryb2tlT3BhY2l0eTogMS4wLA0KICAgICAgICAgIHN0cm9rZVdlaWdodDogMg0KICAgICAgICB9KTsNCg0KCXZhciBtYXJrZXJzID0gdmFsdWVzLm1hcCgodixpKSA9PiAobmV3IGdvb2dsZS5tYXBzLk1hcmtlcih7DQogICAgICAgICAgcG9zaXRpb246IHtsYXQ6IHZbMF0gLCBsbmc6IHZbMV0gfSwNCiAgICAgICAgICBtYXA6IG1hcCwNCiAgICAgICAgICB0aXRsZTogKCh2YWx1ZSwgaW5kZXgsIHZhbHVlcykgPT4ge30gKSh2LCBpLCAgdmFsdWVzKQ0KICAgICAgICB9KSkpOw0KDQogICAgICAgIGZsaWdodFBhdGguc2V0TWFwKG1hcCk7DQogICAgICB9DQogICAgPC9zY3JpcHQ+DQogICAgPHNjcmlwdCBhc3luYyBkZWZlcg0KICAgIHNyYz0iaHR0cHM6Ly9tYXBzLmdvb2dsZWFwaXMuY29tL21hcHMvYXBpL2pzP2tleT17fSZjYWxsYmFjaz1pbml0TWFwIj4NCgk8L3NjcmlwdD4NCiAgPC9ib2R5Pg0KPC9odG1sPg0K"
htmlTemplate = base64.b64decode(htmlTemplate).decode("utf-8")

moves = "[{}]".format(','.join(("[{},{}]".format(move[0], move[1])) for move in solution.tour))
positionCenterCamera = [0,0]
for point in solution.tour:
	for i, latLong in enumerate(positionCenterCamera):
		positionCenterCamera[i] = latLong + point[i]
movesLength = len(solution.tour)
for i, latLong in enumerate(positionCenterCamera):
	positionCenterCamera[i] = latLong / movesLength

positionCamera = positionCenterCamera if MAP_CENTER else solution.tour[0]
mapZoom = 7 if MAP_CENTER else 15

htmlTemplate = re.sub(r'([{}])(?![{} &])', r'\1\1', htmlTemplate)
htmlTemplate = htmlTemplate.format(moves, mapZoom, positionCamera[0], positionCamera[1], "`Point numero ${index + 1} / ${values.length}`", GOOGLE_API_TOKEN)

with open('data/map.html', 'w', newline='') as html:
	html.write(htmlTemplate)

print("Map generated")
print("Starting map")

os.system("start ./data/map.html")
