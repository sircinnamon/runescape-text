from PIL import Image, ImageDraw,ImageFont
def parse_string(input):
	global effect
	global advcolour
	global colour
	has_effect=False
	has_colour=False
	while(":" in input):
		spl = input.split(":",1);
		print("Parsing arg "+spl[0])
		if(spl[0] in colourmap and has_colour==False):
			print("Set colour to "+spl[0])
			has_colour = True
			colour = spl[0]
			input=spl[1]
		elif(spl[0] in advcolourmap and has_colour==False):
			print("Set advcolour to "+spl[0])
			has_colour = True
			advcolour = spl[0]
			input=spl[1]
		elif(spl[0] in effectmap and has_effect==False):
			print("Set effect to "+spl[0])
			has_effect=True
			effect=spl[0]
			input=spl[1]
		else:
			break
	print("final str "+input)
	effectmap[effect](input)

def single_frame_save(img):
	img.save('test.gif', 'GIF', transparency=0)

def multi_frame_save(img_set, frametime=100):
	img_set[0].save('test.gif', 'GIF', transparency=0, append_images=img_set[1:], save_all=True, duration=frametime, loop=0, disposal=2)

def no_effect(string):
	if(advcolour=="none"):
		size = fnt.getsize(string)
		img = Image.new('RGBA', (size[0]+32, 100), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.text((16,45), string, font=fnt, fill=colourmap[colour])
		single_frame_save(img)
	else:
		size = fnt.getsize(string)
		img = Image.new('RGBA', (size[0]+32, 100), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		draw.text((16,45), string, font=fnt, fill=colourmap[colour])
		single_frame_save(img)

def scroll_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	x_offset = 0
	x_increment = max(round(size[0]/30), 3)
	frame = 0
	while(x_offset < (size[0]*2)+4):
		img = Image.new('RGBA', (size[0], size[1]+4), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		if(advcolour=="none"):
			draw.text((size[0]+1-x_offset,2), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((size[0]+1-x_offset,2), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		x_offset=x_offset+x_increment
		frame = frame+1
	multi_frame_save(img_set)

def slide_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	y_offset = 0
	y_increment = max(round(size[1]/10), 2)
	frame = 0
	while(y_offset < size[1]):
		img = Image.new('RGBA', (size[0], size[1]), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		if(advcolour=="none"):
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	for i in range(1,11):
		img = Image.new('RGBA', (size[0], size[1]), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		if(advcolour=="none"):
			draw.text((0,-size[1]+y_offset), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((0,-size[1]+y_offset), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		frame = frame+1
	while(y_offset < (size[1]*2)+4):
		img = Image.new('RGBA', (size[0], size[1]), (255, 0, 0, 0))
		draw = ImageDraw.Draw(img)
		if(advcolour=="none"):
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	multi_frame_save(img_set)
	
def wave_effect(string):
	size = fnt.getsize(string)
	img = Image.new('RGBA', (size[0]+32, 100), (255, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	draw.text((16,45), string, font=fnt, fill=colourmap[colour])
	single_frame_save(img)

def wave2_effect(string):
	size = fnt.getsize(string)
	img = Image.new('RGBA', (size[0]+32, 100), (255, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	draw.text((16,45), string, font=fnt, fill=colourmap[colour])
	single_frame_save(img)

def shake_effect(string):
	size = fnt.getsize(string)
	img = Image.new('RGBA', (size[0]+32, 100), (255, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	draw.text((16,45), string, font=fnt, fill=colourmap[colour])
	single_frame_save(img)

def flash1_colour(frame):
	if(frame % fps*2 > fps):
		return colourmap["red"]
	else:
		return colourmap["yellow"]
def flash2_colour(frame):
	if(frame % fps*2 > fps):
		return colourmap["cyan"]
	else:
		return (0,0,255)
def flash3_colour(frame):
	if(frame % fps*2 > fps):
		return colourmap["green"]
	else:
		return (0,255,0)
def glow1_colour(frame):
	return (255,0,0)
def glow2_colour(frame):
	return (255,0,0)
def glow3_colour(frame):
	return (255,0,0)

colour = "yellow"
advcolour = "none"
effect = "none"
fps = 10
colourmap = {
	"yellow": (255,255,0),
	"white": (255,255,255),
	"cyan": (0,255,255),
	"red": (255,0,0),
	"green": (0,128,0),
	"purple": (128,0,128)
}
advcolourmap = {
	"flash1": flash1_colour,
	"flash2": flash2_colour,
	"flash3": flash3_colour,
	"glow1": glow1_colour,
	"glow2": glow2_colour,
	"glow3": glow3_colour,
}
effectmap = {
	"none": no_effect,
	"scroll": scroll_effect,
	"slide": slide_effect,
	"wave": wave_effect,
	"wave2": wave2_effect,
	"shake": shake_effect
}

string = "flash2:slide:Aaron does this look right to you"
fnt = ImageFont.truetype('./runescape_uf.ttf', size=15)

parse_string(string)