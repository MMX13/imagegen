from PIL import Image
from collections import namedtuple
import math
from pprint import pprint
from random import randint
from collections import deque

#2 40
point = namedtuple("Point", "target current distance")
#min_width = 2
#max_width = 40
widths = deque([100])
BASE_COLOR = (255,255,255)
img_w = 0
img_h = 0
NUM_CHILDREN = 1

def get_distance(o, d):
	return math.sqrt((d[0]-o[0])**2 + (d[1]-o[1])**2 + (d[2]-o[2])**2)

def get_current_data(points):
	data = []
	for h in range(im.size[1]):
		for w in range(im.size[0]):
			data.append(points[h][w].current)
	return data

im = Image.open("input.jpg")
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

while(True):

	candidate = None
	best = 0

	for c in range(NUM_CHILDREN):
		origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
		#size = randint(min_width,max_width)
		cur_width = widths[randint(0, len(widths)-1)]
		deviance = math.ceil(cur_width/10.0)+4
		min_width = 2 if cur_width-deviance<2 else cur_width-deviance
		size = randint(min_width, cur_width+deviance)
		
		fidelity = int(math.floor(math.sqrt(size)))
		colour = colours[randint(0, len(colours)-1)]

		sum_distances = 0
		distances = 0
		new_distances = []
		cur_distances = []
		for h in range(size):
			new_distances.append([])
			for w in range(size):
				if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
					if h%fidelity==0:# and w%fidelity==0:
						distances += 1
						new_distance = get_distance(colour, progress[h+origin[1]][w+origin[0]].target)
						new_distances[h].append(new_distance)
						sum_distances += new_distance
						cur_distances.append(progress[h+origin[1]][w+origin[0]].distance)
					new_distances[h].append(None)
		avg_distance = sum_distances/distances				
		cur_distance = sum(cur_distances)/distances


		if sum_distances < sum(cur_distances):
			improvement = sum(cur_distances) - sum_distances
			if improvement > best:
				candidate = (origin, size, colour, new_distances)
		# if avg_distance < cur_distance:
		# 	improvement = cur_distance - avg_distance
		# 	if improvement > best:
		# 		candidate = (origin, size, colour, new_distances)

	if candidate:
		for h in range(candidate[1]):
			for w in range(candidate[1]):
				if h+candidate[0][1]<im.size[1] and w+candidate[0][0]<im.size[0]:
					if not candidate[3][h][w]:
						candidate[3][h][w] = get_distance(candidate[2], progress[h+candidate[0][1]][w+candidate[0][0]].target)
					progress[h+candidate[0][1]][w+candidate[0][0]] = point(progress[h+candidate[0][1]][w+candidate[0][0]].target, candidate[2], candidate[3][h][w])
		

		paste = Image.new(mode="RGB", size=(candidate[1],candidate[1]), color=candidate[2])
		new.paste(paste, candidate[0])
		successes += 1
		widths.append(candidate[1])
		#if len(widths)>queue_length:
		#	widths.popleft()


		if successes%50==0:
			print sum(widths)/len(widths)
			out+=1
			new.save("out/output{}.jpg".format(out))
	else:
		if len(widths)>100:
			widths.popleft()

	if out==2000:
		break


#for each pixel, store target, current and distance


#create new image
#draw polygon
#compare average distance of polygon with existing avg. write polygon if it is better

