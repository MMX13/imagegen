from PIL import Image
from collections import namedtuple
import math
from pprint import pprint
from random import randint

point = namedtuple("Point", "target current distance")
min_width = 2
max_width = 40
BASE_COLOR = (255,255,255)
img_w = 0
img_h = 0

def get_distance(o, d):
	return math.sqrt((d[0]-o[0])**2 + (d[1]-o[1])**2 + (d[2]-o[2])**2)

def get_current_data(points):
	data = []
	for h in range(im.size[1]):
		for w in range(im.size[0]):
			data.append(points[h][w].current)
	return data


im = Image.open("squirrel.jpg")
imdata = im.getdata()
colours = list({c for c in imdata})

progress = [[]]
data_gen = (p for p in imdata)

for h in range(im.size[1]):
	progress.append([])
	for w in range(im.size[0]):
		target = data_gen.next()
		progress[h].append(point(target, BASE_COLOR, get_distance(BASE_COLOR, target)))

successes = 0
out = 0
new = Image.new(mode="RGB", size=im.size, color=BASE_COLOR)

for i in range(1000000):
	origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
	size = randint(min_width,max_width)
	colour = colours[randint(0, len(colours)-1)]

	#current_avg
	#new_avg

	sum_distances = 0
	distances = size**2
	new_distances = []
	cur_distances = []
	for h in range(size):
		new_distances.append([])
		for w in range(size):
			if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
				new_distance = get_distance(colour, progress[h+origin[1]][w+origin[0]].target)
				new_distances[h].append(new_distance)
				sum_distances += new_distance
				cur_distances.append(progress[h+origin[1]][w+origin[0]].distance)
	avg_distance = sum_distances/distances				
	cur_distance = sum(cur_distances)/distances

	if avg_distance < cur_distance:
		for h in range(size):
			for w in range(size):
				if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
					progress[h+origin[1]][w+origin[0]] = point(progress[h+origin[1]][w+origin[0]].target, colour, new_distances[h][w])
		

		paste = Image.new(mode="RGB", size=(size,size), color=colour)
		new.paste(paste, origin)
		successes += 1

		if successes%16==0:
			out+=1
			new.save("output/squirrel{}.jpg".format(out))


#for each pixel, store target, current and distance


#create new image
#draw polygon
#compare average distance of polygon with existing avg. write polygon if it is better

