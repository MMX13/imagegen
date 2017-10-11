from PIL import Image
from collections import namedtuple
import math
from pprint import pprint
from random import randint

point = namedtuple("Point", "target current distance")
min_width = 2
max_width = 50
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

for i in range(1000000):
	origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
	size = randint(min_width,max_width)
	colour = colours[randint(0, len(colours)-1)]

	#current_avg
	#new_avg
	distances = []
	for h in range(size):
		for w in range(size):
			if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
				distances.append(get_distance(colour, progress[h+origin[1]][w+origin[0]].target))
	avg_distance = sum(distances)/len(distances)

	cur_distances = []
	for h in range(size):
		for w in range(size):
			if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
				cur_distances.append(get_distance(progress[h+origin[1]][w+origin[0]].current, progress[h+origin[1]][w+origin[0]].target))
	cur_distance = sum(cur_distances)/len(cur_distances)

	if avg_distance < cur_distance:
		for h in range(size):
			for w in range(size):
				if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
					progress[h+origin[1]][w+origin[0]] = point(progress[h+origin[1]][w+origin[0]].target, colour, 0)
		new = Image.new(mode="RGB", size=im.size, color=(0,0,0))
		new.putdata(get_current_data(progress))
		new.save("squirrel{}.jpg".format(i))


#for each pixel, store target, current and distance


#create new image
#draw polygon
#compare average distance of polygon with existing avg. write polygon if it is better

