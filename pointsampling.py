import bpy
import math
import random

population = 200

def random_point(A, B, C):

	u = random.uniform(0.0, 1.0)
	v = random.uniform(0.0, 1.0)
	
	if (u + v) <= 1:
		
		random_point.result = (B - A) * u + (C - A) * v + A
		
	else:
		
		# flip the direction
		u = 1 - u
		v = 1 - v
		
		random_point.result = (B - A) * u + (C - A) * v + A
		
context = bpy.context

selection = context.selected_objects

active_canvas = selection[1]
active_instance = selection[0]

# get all polygons, their areas, vertices

polylist = [] #get all polys and put them in a list
arealist = [] # list to store area of polys

for poly in active_canvas.data.polygons:
	
	polyarea = poly.area # get area of polygon
	arealist.append(polyarea)
	vertlist = []

	for loop_index in poly.vertices:  # iterate through all vertices on every face index

		# iterate through all vertices, multiply it to world space
		k = (active_canvas.matrix_world @ active_canvas.data.vertices[loop_index].co)  # append vertices to list
		vertlist.append(k)
		
	polylist.append(vertlist)

# cumulative distribution:

# sort arealist
sortedareas = arealist[:]
sortedareas.sort()
smallest_area = sortedareas[0]
cumul_distribution = []

# step through all area values in arealist and divide with the smallest area
for o in range(len(arealist)):
	
	divide_by_smallest= math.ceil(arealist[o] / smallest_area)
	cumul_distribution.append(divide_by_smallest)
	
polypicklist = []

for u in range(len(cumul_distribution)):
	
	list_step = cumul_distribution[u]
	
	for g in range(list_step):
		
		distrib_polylist = polylist[u]
		polypicklist.append(distrib_polylist)
		
	pointlist = []

for t in range(population):
	
	polychoice = random.choice(polypicklist)

	random_point(polychoice[0], polychoice[1], polychoice[2])
	pointlist.append(random_point.result)

for l in pointlist:
	
	duplicate = active_instance.copy()
	duplicate.data = active_instance.data.copy()
	duplicate.name = active_instance.name + "_instance_"
	
	context.collection.objects.link(duplicate)
	
	duplicate.location = l