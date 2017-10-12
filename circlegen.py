from PIL import Image, ImageDraw
from collections import namedtuple, deque
import math
from random import randint

BASE_COLOR = (255, 255, 255)
NUM_CHILDREN = 1

pixel = namedtuple("Pixel", "target current distance")
diameters = deque([100])
input_path = "squirrel.jpg"


im = Image.open(input_path)
imdata = im.getdata()
colors = list({c for c in imdata})

last_diameter = 10
deviance = 10


def generate_new_circle():
	min_diameter = 5
	max_diameter = 150
	origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
	#min_diameter = 3 if last_diameter-deviance<3 else last_diameter-deviance
	
	#diameter = randint(min_diameter, last_diameter+deviance)
	diameter = randint(min_diameter, max_diameter)
	color = colors[randint(0, len(colors)-1)]
	return (origin, diameter, color)

def init_buffer():
	data_gen = (p for p in imdata)
	for h in range(im.size[1]):
		img_buffer.append([])
		for w in range(im.size[0]):
			target = data_gen.next()
			img_buffer[h].append(pixel(target, BASE_COLOR, get_distance(BASE_COLOR, target)))

def get_distance(o, d):
	return math.sqrt((d[0]-o[0])**2 + (d[1]-o[1])**2 + (d[2]-o[2])**2)

def get_current_data(points):
	data = []
	for h in range(im.size[1]):
		for w in range(im.size[0]):
			data.append(points[h][w].current)
	return data


img_buffer = []
init_buffer()

new = Image.new(mode="RGB", size=im.size, color=BASE_COLOR)

i = 1
while True:	
	new_circle = generate_new_circle()
	fidelity = math.floor(math.sqrt(new_circle[1]))
	circle_box = (new_circle[0][0], new_circle[0][1], new_circle[0][0]+new_circle[1], new_circle[0][1]+new_circle[1])
	temp_image = new.crop(circle_box)
	draw = ImageDraw.Draw(temp_image)
	draw.ellipse((0,0,new_circle[1], new_circle[1]), fill=new_circle[2])

	new_distance = 0
	new_distances = []
	current_distance = 0
	for h in range(new_circle[1]):
		new_distances.append([])
		for w in range(new_circle[1]):
			if h+new_circle[0][1]<im.size[1] and w+new_circle[0][0]<im.size[0]:
				if h%fidelity==0:
					distance = get_distance(temp_image.getpixel((w,h)), img_buffer[h+new_circle[0][1]][w+new_circle[0][0]].target)
					new_distances[h].append(distance)
					new_distance += distance
					current_distance += img_buffer[h+new_circle[0][1]][w+new_circle[0][0]].distance
				else:
					new_distances[h].append(None)

	if new_distance<current_distance:
		for h in range(new_circle[1]):
			for w in range(new_circle[1]):
				if h+new_circle[0][1]<im.size[1] and w+new_circle[0][0]<im.size[0]:
					if new_distances[h][w]==None:
						new_distances[h][w] = get_distance(temp_image.getpixel((w,h)), img_buffer[h+new_circle[0][1]][w+new_circle[0][0]].target)
					img_buffer[h+new_circle[0][1]][w+new_circle[0][0]] = pixel(img_buffer[h+new_circle[0][1]][w+new_circle[0][0]].target, new_circle[2], new_distances[h][w])

		new.paste(temp_image, new_circle[0])
		if i%20==0:			
			new.save("circle/circle{}.jpg".format(i))
		i+=1
		last_diameter = new_circle[1]


# successes = 0
# out = 0
# new = Image.new(mode="RGB", size=im.size, color=BASE_COLOR)

# while(True):

# 	candidate = None
# 	best = 0

# 	for c in range(NUM_CHILDREN):
# 		origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
# 		#size = randint(min_width,max_width)
# 		cur_width = widths[randint(0, len(widths)-1)]
# 		deviance = math.ceil(cur_width/10.0)+4
# 		min_width = 2 if cur_width-deviance<2 else cur_width-deviance
# 		size = randint(min_width, cur_width+deviance)
		
# 		fidelity = int(math.floor(math.sqrt(size)))
# 		colour = colours[randint(0, len(colours)-1)]

# 		sum_distances = 0
# 		distances = 0
# 		new_distances = []
# 		cur_distances = []
# 		for h in range(size):
# 			new_distances.append([])
# 			for w in range(size):
# 				if h+origin[1]<im.size[1] and w+origin[0]<im.size[0]:
# 					if h%fidelity==0:# and w%fidelity==0:
# 						distances += 1
# 						new_distance = get_distance(colour, progress[h+origin[1]][w+origin[0]].target)
# 						new_distances[h].append(new_distance)
# 						sum_distances += new_distance
# 						cur_distances.append(progress[h+origin[1]][w+origin[0]].distance)
# 					new_distances[h].append(None)
# 		avg_distance = sum_distances/distances				
# 		cur_distance = sum(cur_distances)/distances


# 		if sum_distances < sum(cur_distances):
# 			improvement = sum(cur_distances) - sum_distances
# 			if improvement > best:
# 				candidate = (origin, size, colour, new_distances)
# 		# if avg_distance < cur_distance:
# 		# 	improvement = cur_distance - avg_distance
# 		# 	if improvement > best:
# 		# 		candidate = (origin, size, colour, new_distances)

# 	if candidate:
# 		for h in range(candidate[1]):
# 			for w in range(candidate[1]):
# 				if h+candidate[0][1]<im.size[1] and w+candidate[0][0]<im.size[0]:
# 					if not candidate[3][h][w]:
# 						candidate[3][h][w] = get_distance(candidate[2], progress[h+candidate[0][1]][w+candidate[0][0]].target)
# 					progress[h+candidate[0][1]][w+candidate[0][0]] = point(progress[h+candidate[0][1]][w+candidate[0][0]].target, candidate[2], candidate[3][h][w])
		

# 		paste = Image.new(mode="RGB", size=(candidate[1],candidate[1]), color=candidate[2])
# 		new.paste(paste, candidate[0])
# 		successes += 1
# 		widths.append(candidate[1])
# 		#if len(widths)>queue_length:
# 		#	widths.popleft()


# 		if successes%50==0:
# 			print sum(widths)/len(widths)
# 			out+=1
# 			new.save("out/output{}.jpg".format(out))
# 	else:
# 		if len(widths)>100:
# 			widths.popleft()

# 	if out==2000:
# 		break


# #for each pixel, store target, current and distance


# #create new image
# #draw polygon
# #compare average distance of polygon with existing avg. write polygon if it is better

