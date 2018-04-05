#!/usr/bin/env python

import urllib

# GET COLOR FROM IMAGE / BASED ON https://gist.github.com/zollinger/1722663
def getcolor(img):

	from PIL import Image
	
	img = img.resize((150, 150))
	result = img.convert('P', palette=Image.ADAPTIVE, colors=1)
	result.putalpha(255)
	colors = result.getcolors(22500)
	color = colors[0][1]
	
	return color

# SET savein AND saveout PATHS
def setpaths(path, imageurl, usecustomname):

	import os

	imgname = os.path.basename(imageurl)
	filename, file_extension = os.path.splitext(imgname)

	if not file_extension:
		file_extension = '.jpg'

	if usecustomname:
		imgname = str(usecustomname) + file_extension
	
	savein = path + '/' + imgname
	saveout = path + '/' + filename + '_info' + file_extension

	return savein, saveout

# SET THE TEXT ON THE IMAGE
def setimage(savein, saveout, screensize, content, style):

	from pynotify.pynotify import notify

	(headstyle, textstyle, text_wraplength) = style
	(date, title, text) = content

	# CHECK IF PIL/PILLOW IS INSTALLED
	try:
		import PIL
	except ImportError, e:
		notify(
			'Please read the source code.',
			'This thing requires an additional package.',
			'You need Pillow (Python package) to get an image with info.',
			'error'
			)
		pass
	else:

		# GET THE SCREEN SIZE
		(vw, vh) = screensize

		# CALCULATE RATIO OF THE SCREEN
		ratioscreen = float(vw) / vh
		print('Screenratio is %s (%sx%spx).' % (ratioscreen, vw, vh))

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
		print('Imageratio is %s (%sx%spx).' % (ratioimage, width, height))

		# CUT THE IMAGE TO THE SCREEN RATIO
		if ratioscreen > ratioimage:

			newheight = int(floor(width / ratioscreen))

			img = ImageOps.fit(img, (width,newheight), centering = (0.5,0.5))
			(width, height) = img.size

			print 'Image cut.'

		elif ratioscreen < ratioimage:

			newwidth = int(floor(height * ratioscreen))

			img = ImageOps.fit(img, (newwidth,height), centering = (0.5,0.5))
			(width, height) = img.size

			print 'Image cut.'

		# UPSCALE IMAGE TO DISPLAY SIZE
		if width < vw:

			img = img.resize((int(vw), int(vh)), Image.BICUBIC)
			width = vw
			height = vh

			print 'Image upscaled.'
		
		# BEGIN PILLOW'S DRAWING
		overlay = Image.new('RGBA', img.size)
		# draw = ImageDraw.Draw(img)
		draw = ImageDraw.Draw(overlay)

		# IMPORT MORE STUFF
		from PIL import ImageFont
		from math import floor
		import textwrap

		# CALCULATE FONT SIZES
		fsizehead = int(floor(height / headstyle[2]))
		fsizetext = int(floor(height / textstyle[2]))
		
		# WRAP TEXT
		wrapped = textwrap.fill(text, text_wraplength)
		
		# SET FONT STYLES
		headfont = ImageFont.truetype(headstyle[0],fsizehead,index=headstyle[1])
		textfont = ImageFont.truetype(textstyle[0],fsizetext,index=textstyle[1])

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

		# DRAW THE 'text'-TEXT ONTO THE BACKGROUND
		draw.text((x + 1, y + 1),wrapped,invcolor,font=textfont)
		# draw.text((x, y),wrapped,(0,0,0),font=textfont,align="left")

		# DRAW THE HEADING
		draw.text((x, (y - 2 * silver - hhead)),title,invcolor,font=headfont)
		# draw.text((golden, golden),title,(255,255,255),font=headfont)

		# CHANGE LOGINIMAGE
		# (add stuff for changing loginimage)

		# SET THE OVERLAY ON TOP OF THE IMG
		img = Image.alpha_composite(img, overlay)

		print 'Text written.'

		# WRITE THE IMAGE TO saveout
		img.save(saveout)

		print 'Image saved.'

		# SET savein TO saveout SO THE MODIFIED IMAGE IS SET AS BG IN THE NEXT STEP
		savein = saveout

	# RETURN NEW SAVEIN
	return savein

def getimage(imageurl, savein):
	
	# DOWNLOAD THE HQ IMAGE FROM imageurl TO savein
	urllib.urlretrieve(imageurl, savein)
	
	print 'Image has been downloaded.'