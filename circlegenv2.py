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

distance_cache = []

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
	diameter = get_hw_radius()
	#diameter = get_stepped_radius()
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
	return (d[0]-o[0])**2 + (d[1]-o[1])**2 + (d[2]-o[2])**2

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
out = 1
failures = 0
while True:	
	new_circle = generate_new_circle()
	circle_box = (new_circle.origin[0], new_circle.origin[1], new_circle.origin[0]+new_circle.diameter, new_circle.origin[1]+new_circle.diameter)
	target_image = im.crop(circle_box)
	current_image = new.crop(circle_box)
	temp_image = new.crop(circle_box)
	draw = ImageDraw.Draw(temp_image)
	draw.ellipse((0,0,new_circle.diameter, new_circle.diameter), fill=new_circle.color)

	target_data = target_image.getdata()
	temp_data = temp_image.getdata()
	current_data = current_image.getdata()

	new_distance = 0
	current_distance = 0
	fidelity = math.ceil(math.sqrt(new_circle.diameter))

	for p in range(len(target_data)):
		if p%fidelity == 0:
			#if temp_data[p] != current_data[p]:
				new_distance += get_distance(temp_data[p], target_data[p])
				current_distance += get_distance(current_data[p], target_data[p])

	if new_distance<current_distance:
		new.paste(temp_image, new_circle.origin)
		if i%20==0:			
			new.save("out/circle{}.jpg".format(out))
			out+=1
		i+=1
		diameters.append(new_circle.diameter)
		if len(diameters)>100:
			diameters.popleft()
		if i==5000:
			break
	else:
		failures += 1