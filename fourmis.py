#Imports
from random import uniform
from haversine import haversine
import pants
import csv
import os, sys
import requests
from urllib.parse import quote
import matplotlib.pyplot as plt
import networkx as nx

#Constants
CSV_FILENAME = "open_pubs.csv"
#CSV_FILENAME = "london_pubs.csv"
USE_MILES_UNIT = False #if false, will use Kilometers
try:
	GOOGLE_API_TOKEN = os.environ['GOOGLE_API_TOKEN']
except:
	print("You need to define the GOOGLE_API_TOKEN env variable to use GOOGLE GEOLOC API")
	sys.exit(1)

NUMBER_NODES = os.getenv('NUMBER_NODES', 0)

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


print("Create the graph")
G=nx.Graph()
G.add_edges_from(nodes)
nx.draw(G)
plt.show()
print("Finished the graph")

#Code

print("Creating world")
world = pants.World(nodes, calcul_distance)
print("Finished creating world")

print("Creating solver")
solver = pants.Solver()
print("Finished creating solver")

print("Starting solving world")
solutions = solver.solutions(world)
print("Finished solving world")

best = float("inf")
for solution in solutions:
	if solution.distance < best:
		best = solution.distance

print("the best distance is {} {}".format(round(best, 3), "miles" if USE_MILES_UNIT else "km"))
