from PIL import Image, ImageDraw,ImageFont
import math

def parse_string(input, delimiter=':'):
	global effect
	global advcolour
	global colour
	effect = defaulteffect
	colour = defaultcolour
	advcolour = defaultadvcolour
	has_effect=False
	has_colour=False
	while(delimiter in input):
		spl = input.split(delimiter,1);
		# print("Parsing arg "+spl[0])
		if(spl[0] in colourmap and has_colour==False):
			# print("Set colour to "+spl[0])
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
	# print("final str "+input)
	return effectmap[effect](input)

def single_frame_save(img, append=""):
	# img.save('test.gif', 'GIF', transparency=0)
	print("Save test"+append+".gif")
	img.save("test"+append+".gif", 'GIF',transparency=0)
	return "test"+append+".gif"

def multi_frame_save(img_set, frametime=100):
	print("Save test.gif")
	img_set[0].save('test.gif', 'GIF', transparency=0, append_images=img_set[1:], save_all=True, duration=frametime, loop=0, disposal=2, optimize=False)
	return "test.gif"

def no_effect(string):
	print(advcolour)
	if(advcolour=="none"):
		size = fnt.getsize(string)
		img = Image.new('RGBA', (size[0], size[1]+4), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		draw.text((0+1,2+1), string, font=fnt, fill=(0,0,0))
		draw.text((0,2), string, font=fnt, fill=colourmap[colour])
		return single_frame_save(img)
	else:
		size = fnt.getsize(string)
		img_set=[]
		frame = 0
		while(frame < fps*4):
			img = Image.new('RGBA', (size[0], size[1]+4), (255, 255, 255, 0))
			draw = ImageDraw.Draw(img)
			draw.fontmode = "1"
			draw.text((0+1,2+1), string, font=fnt, fill=(0,0,0))
			draw.text((0,2), string, font=fnt, fill=advcolourmap[advcolour](frame))
			img_set.append(img)
			frame = frame+1
		return multi_frame_save(img_set)

def scroll_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	x_offset = 0
	x_increment = max(round(size[0]/30), 3)
	frame = 0
	while(x_offset < (size[0]*2)+4):
		img = Image.new('RGBA', (size[0], size[1]+4), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		if(advcolour=="none"):
			draw.text((1+size[0]+1-x_offset,1+2), string, font=fnt, fill=(0,0,0))
			draw.text((size[0]+1-x_offset,2), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((1+size[0]+1-x_offset,1+2), string, font=fnt, fill=(0,0,0))
			draw.text((size[0]+1-x_offset,2), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		x_offset=x_offset+x_increment
		frame = frame+1
	return multi_frame_save(img_set)

def slide_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	y_offset = 0
	y_increment = max(round(size[1]/10), 2)
	frame = 0
	while(y_offset < size[1]):
		img = Image.new('RGBA', (size[0], size[1]), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		if(advcolour=="none"):
			draw.text((0+1,1+(-size[1]+y_offset)), string, font=fnt, fill=(0,0,0))
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((0+1,1+(-size[1]+y_offset)), string, font=fnt, fill=(0,0,0))
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	for i in range(1,11):
		img = Image.new('RGBA', (size[0], size[1]), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		if(advcolour=="none"):
			draw.text((0+1,1-size[1]+y_offset), string, font=fnt, fill=(0,0,0))
			draw.text((0,-size[1]+y_offset), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((0+1,1-size[1]+y_offset), string, font=fnt, fill=(0,0,0))
			draw.text((0,-size[1]+y_offset), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		frame = frame+1
	while(y_offset < (size[1]*2)+4):
		img = Image.new('RGBA', (size[0], size[1]), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		if(advcolour=="none"):
			draw.text((1+0,1+(-size[1]+y_offset)), string, font=fnt, fill=(0,0,0))
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((1+0,1+(-size[1]+y_offset)), string, font=fnt, fill=(0,0,0))
			draw.text((0,(-size[1]+y_offset)), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	return multi_frame_save(img_set)
	
def wave_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	for f in range(frames):
		img = Image.new('RGBA', (size[0]+(1*len(string)), size[1]*3), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			x = fnt.getsize(string[:i])[0]+(1*i)
			amplitude = (size[1]/3)
			wave = math.sin((((f+1)/(frames))*math.pi*2)+(i*(math.pi/6)))
			y = size[1] + wave*amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				# draw.text((x+10,y+10), string, font=fnt, fill=(8,8,8))
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
				# draw.text((x,y), string[i], font=fnt, fill=(150,150,150))
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return multi_frame_save(img_set)

def wave2_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	for f in range(frames):
		img = Image.new('RGBA', (2+size[0]+(1*len(string)), size[1]*3), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			x_amplitude = size[0]/(len(string)*4)
			y_amplitude = (size[1]/4)
			wave = math.sin((((f+1)/(frames))*math.pi*2)+(i*(math.pi/6)))
			x = 2+fnt.getsize(string[:i])[0] +(1*i)- wave*x_amplitude
			y = size[1] + wave*y_amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return multi_frame_save(img_set)

def shake_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	for f in range(frames):
		img = Image.new('RGBA', (size[0]+(1*len(string)), size[1]*3), (255, 255, 255, 0))
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			x = fnt.getsize(string[:i])[0]+(1*i)
			amplitude = -(size[1]/3)
			current_peak = (f/frames)*100
			if i > current_peak:
				rad = 0
			elif i < current_peak-12:
				rad = 0
			else:
				rad = (math.pi/2)+((current_peak-i)/12)*3.5*math.pi
			wave = math.sin(rad)
			if(rad>(math.pi*1.5)):
				amplitude = amplitude*0.75
			if(rad>(math.pi*2)):
				amplitude = amplitude*0.33
			y = size[1] + wave*amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=(0,0,0))
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return multi_frame_save(img_set)

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
	# red-orange-yellow-green-cyan
	cycle_length = fps*2
	inc = cycle_length/4
	frame=frame%cycle_length
	if(frame>=inc*3):
		# green to cyan
		R=0
		G=128+round(128*((frame%inc)/inc))
		B=round(255*((frame%inc)/inc))
		return (R,G,B)
	elif(frame>=inc*2):
		# yellow to green
		R=255-round(255*((frame%inc)/inc))
		G=255-round(128*((frame%inc)/inc))
		B=0
		return (R,G,B)
	elif(frame>=inc*1):
		# Orange to yellow
		R=255
		G=128+round(128*((frame%inc)/inc))
		B=0
		return (R,G,B)
	else:
		# Red to orange
		R=255
		G=round(128*(frame/inc))
		B=0
		return (R,G,B)
	return (255,0,0)
def glow2_colour(frame):
	# red-pink-purple-blue-purple-
	cycle_length = fps*2
	inc = cycle_length/5
	frame=frame%cycle_length
	if(frame>=inc*4):
		# purple to red
		R=128+round(128*((frame%inc)/inc))
		G=0
		B=128-round(128*((frame%inc)/inc))
		return (R,G,B)
	elif(frame>=inc*3):
		# blue to purple
		R=round(128*((frame%inc)/inc))
		G=0
		B=255-round(128*((frame%inc)/inc))
		return (R,G,B)
	elif(frame>=inc*2):
		# purple to blue
		R=128-round(128*((frame%inc)/inc))
		G=0
		B=255+round(128*((frame%inc)/inc))
		return (R,G,B)
	elif(frame>=inc*1):
		# pink to purple
		R=255-round(128*((frame%inc)/inc))
		G=0
		B=128
		return (R,G,B)
	else:
		# red to pink
		R=255
		G=0
		B=round(128*(frame/inc))
		return (R,G,B)
	return (255,0,0)
def glow3_colour(frame):
	# white-light green-dark green-light green-white-cyan
	cycle_length = fps*2
	inc = cycle_length/5
	frame=frame%cycle_length
	if(frame>=inc*4):
		# white to cyan
		R=255-round(255*((frame%inc)/inc))
		G=255
		B=255
		return (R,G,B)
	elif(frame>=inc*3):
		# light green to white
		R=round(255*((frame%inc)/inc))
		G=255
		B=round(255*((frame%inc)/inc))
		return (R,G,B)
	elif(frame>=inc*2):
		# dark green to light green
		R=0
		G=128+round(128*((frame%inc)/inc))
		B=0
		return (R,G,B)
	elif(frame>=inc*1):
		# light green to dark green
		R=0
		G=255-round(128*((frame%inc)/inc))
		B=0
		return (R,G,B)
	else:
		# white to light green
		R=255
		G=255-round(128*((frame%inc)/inc))
		B=255
		return (R,G,B)
	return (255,0,0)

defaultcolour = "yellow"
defaultadvcolour = "none"
defaulteffect = "none"
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

string = "glow1:wave:cdjquw4 \nAAAA"
fnt = ImageFont.truetype('./runescape_uf.ttf', size=15)

# parse_string(string)