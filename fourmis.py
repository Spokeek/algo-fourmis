#Imports
from random import uniform
from haversine import haversine
import pants
import csv

#Constants
CSV_FILENAME = "open_pubs.csv"
#CSV_FILENAME = "london_pubs.csv"
USE_MILES_UNIT = True #if false, will use Kilometers


nodes = []
def calcul_distance(a, b):
	return haversine(a, b, miles=USE_MILES_UNIT)

with open(CSV_FILENAME, 'r') as csvfile:
	print("Starting csv load and cleaning")
	reader = csv.reader(csvfile, doublequote=True, skipinitialspace=True)
	next(reader, None)
	for index, row in enumerate(reader):
		if row[8] == "":
			with open(CSV_FILENAME, 'r') as secondssvfile:
				for i, line in enumerate(secondssvfile):
					if i == index:
						r = csv.reader([line], doublequote=True, skipinitialspace=True)
						row = next(r)
						break
		nodes.append((float(row[4]), float(row[5])))
print("{} nodes found".format(len(nodes)))
print("Finished csv load")

nodes = [node for i, node in enumerate(nodes) if i < 30]
print("{} clean nodes found".format(len(nodes)))

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
