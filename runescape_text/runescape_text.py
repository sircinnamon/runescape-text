from PIL import Image, ImageDraw,ImageFont
import math
import sys, getopt, os

# Preset colors
black = (0,0,0,255)
transparent = (255, 255, 255, 0)

def parse_string(input, delimiter=':', maxlen=80):
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
			# print("Set advcolour to "+spl[0])
			has_colour = True
			advcolour = spl[0]
			input=spl[1]
		elif(spl[0] in effectmap and has_effect==False):
			# print("Set effect to "+spl[0])
			has_effect=True
			effect=spl[0]
			input=spl[1]
		else:
			break
	# print("final str "+input)
	if(len(input[:maxlen].split("\n"))>1):
		line_arr=[]
		max_line_len=max(len(x) for x in input[:maxlen].split("\n"))
		for line in input[:maxlen].split("\n"):
			line="{line: <{width}}".format(line=line, width=max_line_len)
			line_arr.append(effectmap[effect](line))
		return line_merge(line_arr)
	else:
		return effectmap[effect](input[:maxlen])

def single_frame_save(img, file="out.png", append=""):
	# img.save('test.gif', 'GIF', transparency=0)
	# print("Save {}".format(file))
	p = img.getpalette()
	# First colour in palette is the bg, and should be transparent
	tr = [p[0], p[1], p[2]]
	img = img.convert("RGBA")
	px = img.getdata()

	newpx = []
	for p in px:
	    if p[0] == tr[0] and p[1] == tr[1] and p[2] == tr[2]:
	        newpx.append((tr[0], tr[1], tr[2], 0))
	    else:
	        newpx.append(p)
	img.putdata(newpx)
	img.save(file, 'PNG')
	return file

def multi_frame_save(img_set, file="out.gif", frametime=100):
	# print("Save {}".format(file))
	img_set[0].save(
		file,
		'GIF', transparency=0,
		append_images=img_set[1:],
		save_all=True,
		duration=frametime,
		loop=0,
		disposal=2,
		optimize=False
	)
	return file

def no_effect(string):
	if(advcolour=="none"):
		size = fnt.getsize(string)
		img = Image.new('P', (size[0], size[1]+4), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		x = 0
		y = 2
		draw.text((x+1,y+1), string, font=fnt, fill=black)
		draw.text((x,y), string, font=fnt, fill=colourmap[colour])
		return [img]
	else:
		size = fnt.getsize(string)
		img_set=[]
		frame = 0
		while(frame < fps*4):
			img = Image.new('P', (size[0], size[1]+4), transparent)
			draw = ImageDraw.Draw(img)
			draw.fontmode = "1"
			x = 0
			y = 2
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=advcolourmap[advcolour](frame))
			img_set.append(img)
			frame = frame+1
		return img_set

def scroll_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	x_offset = 0
	x_increment = max(round(size[0]/30), 3)
	frame = 0
	while(x_offset < (size[0]*2)+4):
		img = Image.new('P', (size[0], size[1]+4), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		x = size[0]+1-x_offset
		y = 2
		if(advcolour=="none"):
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		x_offset=x_offset+x_increment
		frame = frame+1
	return img_set

def slide_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	y_offset = 0
	y_increment = max(round(size[1]/10), 2)
	frame = 0
	while(y_offset < size[1]):
		img = Image.new('P', (size[0], size[1]+4), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		x = 0
		y = y_offset-size[1]
		if(advcolour=="none"):
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	for i in range(1,11):
		img = Image.new('P', (size[0], size[1]+4), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		x = 0
		y = y_offset-size[1]
		if(advcolour=="none"):
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		frame = frame+1
	while(y_offset < (size[1]*2)+4):
		img = Image.new('P', (size[0], size[1]+4), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		x = 0
		y = y_offset-size[1]
		if(advcolour=="none"):
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=colourmap[colour])
		else:
			draw.text((x+1,y+1), string, font=fnt, fill=black)
			draw.text((x,y), string, font=fnt, fill=advcolourmap[advcolour](frame))
		img_set.append(img)
		y_offset=y_offset+y_increment
		frame = frame+1
	return img_set
	
def wave_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	amplitude = (size[1]/3)
	for f in range(frames):
		img = Image.new('P', (size[0]+(1*len(string)), round(size[1]+(amplitude*2)+0.5)), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			x = fnt.getsize(string[:i])[0]+(1*i)
			wave = math.sin((((f+1)/(frames))*math.pi*2)+(i*(math.pi/6)))
			y = amplitude + wave*amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				# draw.text((x+10,y+10), string, font=fnt, fill=(8,8,8))
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
				# draw.text((x,y), string[i], font=fnt, fill=(150,150,150))
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return img_set

def wave2_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	x_amplitude = size[0]/(len(string)*4)
	y_amplitude = (size[1]/4)
	for f in range(frames):
		img = Image.new('P', (2+size[0]+(1*len(string)), round(size[1]+(y_amplitude*2)+0.5)), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			wave = math.sin((((f+1)/(frames))*math.pi*2)+(i*(math.pi/6)))
			x = 2+fnt.getsize(string[:i])[0] +(1*i)- wave*x_amplitude
			y = y_amplitude + wave*y_amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return img_set

def shake_effect(string):
	size = fnt.getsize(string)
	img_set=[]
	frames=20
	max_amplitude = size[1]/3
	for f in range(frames):
		img = Image.new('P', (size[0]+(1*len(string)), round(size[1]+(max_amplitude*2)+0.5)), transparent)
		draw = ImageDraw.Draw(img)
		draw.fontmode = "1"
		for i in range(len(string)):
			x = fnt.getsize(string[:i])[0]+(1*i)
			amplitude = -max_amplitude
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
			y = max_amplitude + wave*amplitude
			if(advcolour=="none"):
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				draw.text((x,y), string[i], font=fnt, fill=colourmap[colour])
			else:
				draw.text((x+1,y+1), string[i], font=fnt, fill=black)
				draw.text((x,y), string[i], font=fnt, fill=advcolourmap[advcolour](f))
		img_set.append(img)
	return img_set

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
	c_list = [
		(255,0,0),
		(255,128,0),
		(255,255,0),
		(0,128,0),
		(0,255,255)
	]
	start_c = c_list[math.floor(frame/inc)]
	end_c = c_list[1+math.floor(frame/inc)]
	prog = (frame%inc)/inc
	return calculate_gradient_pos(start_c, end_c ,prog)

def glow2_colour(frame):
	# red-pink-purple-blue-purple-red
	cycle_length = fps*2
	inc = cycle_length/5
	frame=frame%cycle_length
	c_list = [
		(255,0,0),
		(255,0,128),
		(128,0,128),
		(0,0,255),
		(128,0,128),
		(255,0,0)
	]
	start_c = c_list[math.floor(frame/inc)]
	end_c = c_list[1+math.floor(frame/inc)]
	prog = (frame%inc)/inc
	return calculate_gradient_pos(start_c, end_c ,prog)

def glow3_colour(frame):
	# white-light green-dark green-light green-white-cyan
	cycle_length = fps*2
	inc = cycle_length/5
	frame = frame%cycle_length
	c_list = [
		(255,255,255),
		(0,255,0),
		(0,128,0),
		(0,255,0),
		(255,255,255),
		(0,255,255)
	]
	start_c = c_list[math.floor(frame/inc)]
	end_c = c_list[1+math.floor(frame/inc)]
	prog = (frame%inc)/inc
	return calculate_gradient_pos(start_c, end_c ,prog)


def calculate_gradient_pos(start, end, progress):
	r_diff = end[0]-start[0]
	g_diff = end[1]-start[1]
	b_diff = end[2]-start[2]
	return (
		start[0]+round(r_diff*progress),
		start[1]+round(g_diff*progress),
		start[2]+round(b_diff*progress)
	)

def line_merge(arr):
	if(len(arr)==1):
		return arr[0]
	elif(len(arr)>1):
		mergedframes=[]
		frames=zip(arr[0], arr[1])
		for frame in frames:
			width=frame[0].size[0]+frame[1].size[0]
			height=frame[0].size[1]+frame[1].size[1]
			newframe = Image.new('P', (width, height), transparent)
			newframe.paste(frame[0], (0,0))
			newframe.paste(frame[1], (0,frame[0].size[1]))
			mergedframes.append(newframe)
		arr[0]=mergedframes
		del arr[1]
		return line_merge(arr)


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

fnt = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'data/runescape_uf.ttf'), size=18)

if __name__ == "__main__":
	# string = "glow1:wave:cdjquw4 \nAAAA"
	try:
		opts,args = getopt.getopt(sys.argv[1:], "o:c:e:")
		instring = ""
		outfile = "runescapetext.gif"
		allcolours = list(colourmap.keys())+list(advcolourmap.keys())
		for opt, arg in opts:
			if opt == "-o":
				outfile = arg
			elif opt == "-c" and arg in allcolours:
				instring += arg+":"
			elif opt == "-e" and arg in list(effectmap.keys()):
				instring += arg+":"
		instring+=" ".join(args)
		img = parse_string(instring)
		if(len(img)==1):
			single_frame_save(img[0], file=outfile)
		else:
			multi_frame_save(img, file=outfile)
	except getopt.GetoptError:
		print("\nrunescape_text.py [options] <string>")
		print("OPTIONS")
		print("\t-o <outputfile>")
		print("\t-c <colour>")
		print("\t\tAllowed Colors: {}".format(",".join(allcolours)))
		print("\t-e <effect>")
		print("\t\tAllowed Effects: {}".format(",".join(list(effectmap.keys()))))
		sys.exit(2)