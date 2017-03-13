#!/usr/bin/env python

# REQUIREMENTS
# in order to get txt info on the image, you need to do:
#
# $ sudo easy_install pip
# $ (sudo) pip install Pillow
#
# if this is not done, the image (without info) is still being set as new background

# SCHEDULING
# in order to schedule this thing you have to:
#
# > put the getspace.py to /Users/USERNAME/.bin/getspace.py
# > change the USERNAME within the "Program" string in local.getspace.plist
# > add the changed local.getspace.plist into your ~/Library/LaunchAgents
# 
# if this is not (yet) done, you can run the script manually by doing so:
# $ python /path/to/getspace.py

# TODO
# what to do with multi screen setup / different screen sizes?
# http://stackoverflow.com/questions/1281397/how-to-get-the-desktop-resolution-in-mac-via-python

from __future__ import division
import os
import json
import urllib

# OSX SET BACKGROUND
def dosetbackground(path):

	# ######
	# APPLESCRIPT SOLUTION 1
	# does not seem to change more than 1 desktop
	# ######
	# setbackgroundcmd = """
	# osascript -e 'tell application "System Events" to set picture of every desktop to ("{}" as POSIX file as alias)'
	# """

	# ######
	# APPLESCRIPT SOLUTION 2
	# does not seem to change more than 1 desktop
	# ######
	# setbackgroundcmd = """
	# osascript -e 'tell application "System Events"
	# set desktopCount to count of desktops
	# repeat with desktopNumber from 1 to desktopCount
	# 	tell desktop desktopNumber
	# 		set picture to "{}"
	# 	end tell
	# end repeat
	# end tell'
	# """.format(path)

	# ######
	# SQLITE SOLUTION
	# seems to be working though it uses killall Dock and all desktops have to be created from the first
	# ######
	setbackgroundcmd = """
	sqlite3 ~/Library/Application\ Support/Dock/desktoppicture.db "update data set value = '{}'" && killall Dock
	""".format(path)

	os.popen(setbackgroundcmd)

# OSX NOTIFICATION FUNCTION
def notify(title, subtitle, text, sound):
	os.system("""
		osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "{}"'
		""".format(text, title, subtitle, sound))

# DEF GET COLOR BASED ON https://gist.github.com/zollinger/1722663
def getcolor(img):
	img = img.resize((150, 150))
	result = img.convert('P', palette=Image.ADAPTIVE, colors=1)
	result.putalpha(255)
	colors = result.getcolors(22500)
	color = colors[0][1]
	return color

# ENV VARIABLES
home = os.getenv('HOME')
path = home + '/Pictures/GetSpace'

# OPEN URL ON SRV
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
	# imgname = 'testimage.jpg' # for debugging purposes
	imgname = os.path.basename(hdurl)
	savein = path + '/' + imgname
	saveout = path + '/' + 'info_' + imgname

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
		notify("Please read the source code.", "This thing requires a spaceship.", "So, no space info on the desktop for you.", "Basso")
		pass
	else:

		# GET THE SCREEN SIZE
		import AppKit
		# wrong because in a multi screen setup, it would return the size of the last screen in the array
		for screen in AppKit.NSScreen.screens(): 
			vw = screen.frame().size.width
			vh = screen.frame().size.height

		# CALCULATE RATIO OF THE SCREEN
		ratioscreen = vw / vh

		# MANIPULATE THE IMAGE!
		from PIL import Image
		from PIL import ImageOps
		from PIL import ImageFont
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
		ratioimage = width / height

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

		# DEFINE TYPEFACES
		import textwrap

		# 'FUTURA+AVENIR' STYLE
		# SET SIZING VARS
		fsizehead = int(floor(height / 36))
		fsizetext = int(floor(height / 65))
		wrapped = textwrap.fill(explanation, 100)
		# SET FONT VARS
		headfont = ImageFont.truetype("/Library/Fonts/Futura.ttc",fsizehead,index=2)
		textfont = ImageFont.truetype("/System/Library/Fonts/Avenir.ttc",fsizetext)

		# 'MENLO' STYLE
		# SET SIZING VARS
		# fsizehead = int(floor(height / 30))
		# fsizetext = int(floor(height / 70))
		# wrapped = textwrap.fill(explanation, 105)
		# SET FONT VARS
		# headfont = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",fsizehead,index=1)
		# textfont = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",fsizetext)

		# 'GILL SANS' STYLE
		# SET SIZING VARS
		# fsizehead = int(floor(height / 35))
		# fsizetext = int(floor(height / 55))
		# wrapped = textwrap.fill(explanation, 110)
		# SET FONT VARS
		# headfont = ImageFont.truetype("/Library/Fonts/GillSans.ttc",fsizehead,index=1)
		# textfont = ImageFont.truetype("/Library/Fonts/GillSans.ttc",fsizetext,index=7)

		# 'HELVETICA NEUE' STYLE
		# SET SIZING VARS
		# fsizehead = int(floor(height / 30))
		# fsizetext = int(floor(height / 57))
		# wrapped = textwrap.fill(explanation, 100)
		# SET FONT VARS
		# headfont = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.dfont",fsizehead,index=6)
		# textfont = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.dfont",fsizetext,index=1)

		# 'SAN FRANCISCO' STYLE
		# SET SIZING VARS
		# fsizehead = int(floor(height / 35))
		# fsizetext = int(floor(height / 65))
		# wrapped = textwrap.fill(explanation, 105)
		# SET FONT VARS
		# headfont = ImageFont.truetype("/System/Library/Fonts/SFCompactText-Heavy.otf",fsizehead)
		# textfont = ImageFont.truetype("/System/Library/Fonts/SFCompactText-Light.otf",fsizetext)

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

		# ADD ADMIN PAGE PNG
		# dosetbackground(savein)
		# loginimage = '/Library/Caches/com.apple.desktop.admin.png'
		
		# try:
		# 	os.remove(loginimage) # OSX REGENERATES FILE AUTOMATICALLY / or not
		# except OSError:
		# 	pass

		# admin = img.filter(ImageFilter.GaussianBlur(radius=15))
		# admin.save(loginimage)

		# SET THE OVERLAY ON TOP OF THE IMG
		img = Image.alpha_composite(img, overlay)

		# WRITE THE IMAGE TO saveout
		img.save(saveout)

		# SET savein TO saveout SO THE MODIFIED IMAGE IS SET AS BG IN THE NEXT STEP
		savein = saveout


	# SETTING THE DESKTOP BG
	dosetbackground(savein)

	# SETTING 

	notify("Boldly go where only aliens have gone before", title.replace("'", ""), "Background image has been set.", "Submarine")
	
else:

	notify("Space, the final frontier!", "Apparently, there is no new image today.", "Try investing in space travel or something.", "Basso")