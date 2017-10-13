from PIL import Image, ImageDraw
from collections import namedtuple, deque
import math
from random import randint

BASE_COLOR = (255, 255, 255)
NUM_CHILDREN = 1
MIN_DIAMETER = 5
step_radius = 100
pixel = namedtuple("Pixel", "target current distance")
circle = namedtuple("Circle", "origin diameter color")
input_path = "squirrel.jpg"


im = Image.open(input_path)
imdata = im.getdata()
colors = list({c for c in imdata})

diameters = deque([im.size[0]/4])


def get_hw_radius():
	base_diameter = diameters[randint(0, len(diameters)-1)]
	deviance = base_diameter/4
	min_diameter = MIN_DIAMETER if base_diameter-deviance<MIN_DIAMETER else base_diameter-deviance
	max_diameter = MIN_DIAMETER if base_diameter+deviance<MIN_DIAMETER else base_diameter+deviance
	return randint(min_diameter, max_diameter)

def get_stepped_radius():
	global step_radius
	global failures
	if failures > 50:
		failures = 0
		new = step_radius-1
		step_radius = new if new >= MIN_DIAMETER else MIN_DIAMETER
	return step_radius

def generate_new_circle():
	origin = (randint(0, im.size[0]-1), randint(0, im.size[1]-1))
	#diameter = get_hw_radius()
	diameter = get_stepped_radius()
	color = colors[randint(0, len(colors)-1)]
	return circle(origin, diameter, color)

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
failures = 0
while True:	
	new_circle = generate_new_circle()
	fidelity = 2
	#fidelity = math.ceil(math.sqrt(new_circle.diameter))
	circle_box = (new_circle.origin[0], new_circle.origin[1], new_circle.origin[0]+new_circle.diameter, new_circle.origin[1]+new_circle.diameter)
	temp_image = new.crop(circle_box)
	draw = ImageDraw.Draw(temp_image)
	draw.ellipse((0,0,new_circle.diameter, new_circle.diameter), fill=new_circle.color)

	new_distance = 0
	new_distances = []
	current_distance = 0
	for h in range(new_circle.diameter):
		new_distances.append([])
		for w in range(new_circle.diameter):
			if h+new_circle.origin[1]<im.size[1] and w+new_circle.origin[0]<im.size[0]:
				if h%fidelity==0 and w%fidelity==0:
					distance = get_distance(temp_image.getpixel((w,h)), img_buffer[h+new_circle.origin[1]][w+new_circle.origin[0]].target)
					new_distances[h].append(distance)
					new_distance += distance
					current_distance += img_buffer[h+new_circle.origin[1]][w+new_circle.origin[0]].distance
				else:
					new_distances[h].append(None)

	if new_distance<current_distance:
		print(failures, step_radius)
		failures = 0
		for h in range(new_circle.diameter):
			for w in range(new_circle.diameter):
				if h+new_circle.origin[1]<im.size[1] and w+new_circle.origin[0]<im.size[0]:
					if new_distances[h][w]==None:
						new_distances[h][w] = get_distance(temp_image.getpixel((w,h)), img_buffer[h+new_circle.origin[1]][w+new_circle.origin[0]].target)
					img_buffer[h+new_circle.origin[1]][w+new_circle.origin[0]] = pixel(img_buffer[h+new_circle.origin[1]][w+new_circle.origin[0]].target, new_circle.color, new_distances[h][w])

		new.paste(temp_image, new_circle.origin)
		if i%20==0:			
			new.save("out/circle{}.jpg".format(i))
		i+=1
		diameters.append(new_circle.diameter)
		if len(diameters)>100:
			diameters.popleft()
		if i==20000:
			break
	else:
		failures += 1