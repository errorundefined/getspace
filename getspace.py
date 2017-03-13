#!/usr/bin/env python

import os
import json
import urllib

# ENV VARIABLE
home = os.getenv('HOME')

# GET OS VARIABLE
from sys import platform

# CONDITIONALLY SET OS SPECIFIC ENV
if platform == 'linux' or platform == 'linux2':

	print 'getspace is NOT YET running as getspace_linux'
	quit() # exit until draft is no draft any longer
	
	import getspace_linux as getspace
	path = home + '/GetSpace'

elif platform == 'darwin':

	print 'getspace is running as getspace_osx'
	
	import getspace_osx as getspace
	path = home + '/Pictures/GetSpace'

else:

	print 'exiting (no compatible os found)'
	quit()

# DEF GET COLOR BASED ON https://gist.github.com/zollinger/1722663
def getcolor(img):
	img = img.resize((150, 150))
	result = img.convert('P', palette=Image.ADAPTIVE, colors=1)
	result.putalpha(255)
	colors = result.getcolors(22500)
	color = colors[0][1]
	return color

# OPEN URL ON SRV - ADD YOUR API KEY HERE
response = urllib.urlopen('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

# LOAD JSON DATA
json = json.load(response)
media_type = (json['media_type'])

# IF AN IMAGE IS AVAILABLE
if media_type == 'image':

	# IF 'PICTURES/GETSPACE' DOES NOT EXISTS, CREATE IT
	if not os.path.exists(path):
		os.makedirs(path)

	# EXTRACT VARIABLES FROM JSON DATA
	date = (json['date'])
	title = (json['title'])
	explanation = (json['explanation'])
	hdurl = (json['hdurl'])
	# (maybe there's not always a HQ version? if so, add fallback for 'url')

	# DEFINE FILE PATH VARIABLES
	imgname = os.path.basename(hdurl)
	filename, file_extension = os.path.splitext(imgname)
	savein = path + '/' + imgname
	saveout = path + '/' + filename + '_info' + file_extension

	# CHECK IF IMAGE IS NEW
	lastspace = path + '/lastspace.txt'
	if os.path.exists(lastspace):
		lastimage = open(lastspace, 'r')
		if lastimage.read() == imgname:
			file = open(lastspace, 'w')
			file.write(imgname) 
			file.close()
			quit()
	else:
		file = open(lastspace, 'w')
		file.write(imgname) 
		file.close()

	# DOWNLOAD THE HQ IMAGE FROM hdurl TO savein
	urllib.urlretrieve(hdurl, savein)

	# CHECK IF PIL/PILLOW IS INSTALLED
	try:
		import PIL
	except ImportError, e:
		getspace.notify("Please read the source code.", "This thing requires a spaceship.", "So, no space info on the desktop for you.", "Basso")
		pass
	else:

		# GET THE SCREEN SIZE
		(vw, vh) = getspace.getscreensize()

		# CALCULATE RATIO OF THE SCREEN
		ratioscreen = vw / vh

		# MANIPULATE THE IMAGE!
		from PIL import Image
		from PIL import ImageOps
		from PIL import ImageDraw
		# from PIL import ImageFilter

		Image.MAX_IMAGE_PIXELS = 1000000000                                                              

		from math import floor

		# OPEN IMG + INVERSION IMAGE
		img = Image.open(savein)
		inv = ImageOps.invert(img)

		# GET IMG + INVERSION COLOR
		imgcolor = getcolor(img)
		invcolor = getcolor(inv)

		# ADDING TRANSPARENCY TO IMGCOLOR
		lst = list(imgcolor)
		lst[3] = 180
		imgcolor = tuple(lst)

		# SET INVCOLOR TO EITHER BLACK OR WHITE
		lst = list(invcolor)
		if lst[0] + lst[1] + lst[2] > 382:
			lst[0] = 255
			lst[1] = 255
			lst[2] = 255
		else:
			lst[0] = 0
			lst[1] = 0
			lst[2] = 0
		invcolor = tuple(lst)

		# OPEN DOWNLOADED IMAGE
		img = img.convert('RGBA')

		# GET IMAGE SIZE
		(width, height) = img.size

		# CALCULATE RATIO OF THE IMAGE
		ratioimage = float(width) / height

		# CUT THE IMAGE TO THE SCREEN RATIO
		if ratioscreen > ratioimage:

			newheight = floor(width / ratioscreen)
			img = ImageOps.fit(img, (width,newheight), centering = (0.5,0.5))
			(width, height) = img.size

		elif ratioscreen < ratioimage:

			newwidth = floor(height * ratioscreen)
			img = ImageOps.fit(img, (newwidth,height), centering = (0.5,0.5))
			(width, height) = img.size
		
		# BEGIN PILLOW'S DRAWING
		overlay = Image.new('RGBA', img.size)
		# draw = ImageDraw.Draw(img)
		draw = ImageDraw.Draw(overlay)

		# GET FONT VARIABLES
		(fsizehead, fsizetext, wrapped, headfont, textfont) = getspace.getfontvars(height, explanation)

		# CALCULATE THE HEADING SIZE
		whead, hhead = draw.textsize(title,font=headfont)

		# SET POSITIONG VARS
		golden = hhead * 1.618
		silver = golden - hhead

		# CALCULATE THE TEXT SIZE AND DEDUCE POSITIONING VARS FOR NEXT 2 STEPS
		wtext, htext = draw.textsize(wrapped,font=textfont)
		x = (2 * golden - silver)
		y = (height - htext - golden - silver)
		x2 = (x + wtext + silver)
		y2 = (y + htext + silver)

		# DRAW A RECTANGULAR BACKGROUND SHAPE ONTO THE IMAGE
		# draw.rectangle([x - silver, y - silver, x2, y2 ],fill=(255,255,255,188))
		draw.rectangle([x - silver, y - silver, x2, y2 ],fill=imgcolor)

		# DRAW THE 'EXPLANATION'-TEXT ONTO THE BACKGROUND
		draw.text((x + 1, y + 1),wrapped,invcolor,font=textfont,align="left")
		# draw.text((x, y),wrapped,(0,0,0),font=textfont,align="left")

		# DRAW THE HEADING
		draw.text((x, (y - 2 * silver - hhead)),title,invcolor,font=headfont)
		# draw.text((golden, golden),title,(255,255,255),font=headfont)

		# CHANGE LOGINIMAGE
		# (add stuff for changing loginimage)

		# SET THE OVERLAY ON TOP OF THE IMG
		img = Image.alpha_composite(img, overlay)

		# WRITE THE IMAGE TO saveout
		img.save(saveout)

		# SET savein TO saveout SO THE MODIFIED IMAGE IS SET AS BG IN THE NEXT STEP
		savein = saveout


	# SETTING THE DESKTOP BG
	getspace.dosetbackground(savein)

	# SETTING 

	getspace.notify("Boldly go where only aliens have gone before", title.replace("'", ""), "Background image has been set.", "Submarine")
	
else:

	getspace.notify("Space, the final frontier!", "Apparently, there is no new image today.", "Try investing in space travel or something.", "Basso")