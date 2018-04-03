#!/usr/bin/env python

# brought to you by error:undefined design
# 
# w: https://error-undefined.de
# g: https://github.com/errorundefined
# b: https://behance.net/errorundefined
# 
# This is part of the APOD client getspace.
# Get the latest version here on Github:
# https://github.com/errorundefined/getspace

import os
# import ssl
import json
import urllib

from lib.pynotify.pynotify import notify

# ENV VARIABLE
home = os.getenv('HOME')

# GET OS VARIABLE
from sys import platform as os_type

# CONDITIONALLY SET OS SPECIFIC ENV..
# ..IF OSX/MACOS:
if os_type == 'darwin':
	
	# ..IMPORT MODULES
	from lib.getspace_osx import getscreensize, setwallpaper

	# ..SET ENV
	path = home + '/Pictures/GetSpace'

	# ..SET STYLE
	headstyle = ('/Library/Fonts/Futura.ttc', 2, 36)
	textstyle = ('/System/Library/Fonts/Avenir.ttc', 0, 65)
	explanation_wraplength = 100

	# ..AND STDOUT.
	print 'getspace is running on OSX/macOS'

# ..IF LINUX:
elif os_type in ['linux', 'linux2']:

	# ..IMPORT MODULES
	from platform import linux_distribution
	distro = linux_distribution()[0]

	# ..SET ENV
	path = home + '/GetSpace' # ?? (maybe correct with home = os.path.expanduser('~') ??)

	# ..AND GO INTO DETAILS:
	# ..IF ELEMENTARY OS
	if 'elementary' in distro:

		# ..IMPORT MODULES
		from lib.getspace_linux import getscreensize
		from lib.getspace_linux_elementary import setwallpaper

		# ..SET STYLE
		headstyle = ('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-ExtraBold.ttf', 0, 45)
		textstyle = ('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-Light.ttf', 0, 55)
		explanation_wraplength = 100

		# ..AND STDOUT.
		print 'getspace is running as getspace_linux_elementary -- there may be bugs'

	else:

		# from lib.getspace_linux import notify, getscreensize, getfontvars, setwallpaper

		print 'getspace does not yet fully support most linux versions'
		quit() # exit - until draft is no draft any longer
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
url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY' # (for video testing: '&date=2018-03-18')

try:
	response = urllib.urlopen(url)

	# LOAD JSON DATA FROM OBJECT
	jsonstuff = json.load(response)

except IOError, e:

	print 'Using CURL fallback.'

	import subprocess

	process = subprocess.Popen(['curl', url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	response = stdout
	
	# LOAD JSON DATA FROM STRING
	jsonstuff = json.loads(response)


# CHECK IF JSON DATA EXISTS
if 'jsonstuff' not in locals():
	print 'Failed! APOD info could not be downloaded.'
	quit()

else:
	print 'APOD info downloaded.'
	media_type = (jsonstuff['media_type'])

# CHECK IF AN VIDEO OR IMNAGE IS AVAILABLE
if media_type == 'video':

	videourl = (jsonstuff['url'])

	from lib.pyquestion.pyquestion import getuserconsent
	from lib.pytoclipboard.pytoclipboard import setclipboard

	if getuserconsent('There is an APOD video today - do you want to see it now?', 'Getspace has the ultimate question to the universe!'):

		import webbrowser

		webbrowser.open_new_tab(videourl)

		notify('Space traveling now..', 'There is an APOD video today.', 'Getspace opened the video link in your browser.', 'success')
		print 'APOD video opened in browser.'

	else:

		setclipboard(videourl)
		notify('Space traveling now..', 'There is an APOD video today.', 'Getspace copied the video link to the clipboard.', 'success')
		print 'APOD video link in clipboard.'

elif media_type == 'image':

	# IF 'PICTURES/GETSPACE' DOES NOT EXISTS, CREATE IT
	if not os.path.exists(path):
		os.makedirs(path)

	# EXTRACT VARIABLES FROM JSON DATA
	date = (jsonstuff['date'])
	title = (jsonstuff['title'])
	explanation = (jsonstuff['explanation'])
	explanation = explanation.replace('Explore the Universe: Random APOD Generator','')
	explanation = explanation.replace('Follow APOD on: Facebook,  Google Plus,  Instagram, or Twitter','')
	hdurl = (jsonstuff['hdurl'])
	# (maybe there's not always a HQ version? if so, add fallback for 'url')

	# DEFINE FILE PATH VARIABLES
	imgname = os.path.basename(hdurl)
	# imgname = 'testimage2.jpg' # debugging
	filename, file_extension = os.path.splitext(imgname)
	savein = path + '/' + imgname
	saveout = path + '/' + filename + '_info' + file_extension

	# CHECK IF IMAGE IS NEW
	lastspace = path + '/lastspace.txt'
	if os.path.exists(lastspace):
		lastimage = open(lastspace, 'r')
		print 'lastimg is: ' + lastimage.read()
		print 'imgname is: ' + imgname
		if lastimage.read() == imgname:
			file = open(lastspace, 'w')
			file.write(imgname)
			file.close()
			print 'exiting (there\'s no new image available)'
			quit()
	else:
		file = open(lastspace, 'w')
		file.write(imgname)
		file.close()

	# DOWNLOAD THE HQ IMAGE FROM hdurl TO savein
	urllib.urlretrieve(hdurl, savein)
	print 'APOD image downloaded.'

	# CHECK IF PIL/PILLOW IS INSTALLED
	try:
		import PIL
	except ImportError, e:
		notify('Please read the source code.', 'This thing requires a spaceship.', 'So, no space info on the desktop for you.', 'error')
		pass
	else:

		# GET THE SCREEN SIZE
		(vw, vh) = getscreensize()

		# CALCULATE RATIO OF THE SCREEN
		ratioscreen = float(vw) / vh
		print('Screenratio is %s (%sx%spx)' % (ratioscreen, vw, vh))

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
		print('Imageratio is %s (%sx%spx)' % (ratioimage, width, height))

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
		wrapped = textwrap.fill(explanation, explanation_wraplength)
		
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

		# DRAW THE 'EXPLANATION'-TEXT ONTO THE BACKGROUND
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


	# SETTING THE DESKTOP BG
	setwallpaper(savein)

	print 'Background set.'

	# SETTING 

	notify('Boldly go where only aliens have gone before', title.replace("'", ""), 'Background image has been set.', 'success')
	
else:

	notify('Space, the final frontier!', 'Apparently, there is no new image today.', 'Try investing in space travel or something.', 'error')