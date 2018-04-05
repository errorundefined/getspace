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
import datetime

from lib.lib_getter import getjson, getenvironment
from lib.pynotify.pynotify import notify

##################################
# PREPARATIONS
##################################
# SET IDENTY AND SOURCE FOR SCRIPT
scriptname = 'getspace'
saveinfolder = 'GetSpace'

# SET SITUATION IN SPACETIME
d = datetime.date.today()
year = d.strftime('%Y')
month = d.strftime('%m')

# GET ENVIRONMENT VARIABLE
(osenvironment, path, style) = getenvironment(scriptname, saveinfolder)

##################################
# PLATFORM DEPENDENT MODULES
##################################
if not osenvironment:
	print 'exiting (no compatible os found)'
	quit()

elif osenvironment == 'macos':
	from lib.os_macos import getscreensize, setwallpaper

elif osenvironment == 'elementary':
	from lib.os_linux import getscreensize
	from lib.os_linux_elementary import setwallpaper

##################################
# SET AND GET JSON
##################################
# SET MAIN JSON FEED
url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY' # (for video testing: '&date=2018-03-18')

# GET JSON DATA
json = getjson(url)

##################################
# START LOGIC SPECIFIC TO GETSPACE
##################################
media_type = (json['media_type'])

##################################
# IF VIDEO IS AVAILABLE
##################################
if media_type == 'video':

	videourl = (json['url'])

	from lib.pyquestion.pyquestion import getuserconsent
	from lib.pytoclipboard.pytoclipboard import setclipboard

	if getuserconsent('There is an APOD video today - do you want to see it now?', 'Getspace has the ultimate question to the universe!'):

		import webbrowser

		webbrowser.open_new_tab(videourl)

		notify(
			'Space traveling now..',
			'There is an APOD video today.',
			'Getspace opened the video link in your browser.',
			'success'
			)
		
		print 'APOD video opened in browser.'

	else:

		setclipboard(videourl)
		
		notify(
			'Space traveling now..',
			'There is an APOD video today.',
			'Getspace copied the video link to the clipboard.',
			'success'
			)
		
		print 'APOD video link in clipboard.'

##################################
# IF IMAGE IS AVAILABLE
##################################
elif media_type == 'image':

	from lib.lib_image import setpaths, getimage, setimage

	# GET DATE
	date = (json['date'])

	# GET IMAGE URL
	imageurl = (json['hdurl'])

	# GET AND CLEAN UP TEXT
	text = (json['explanation'])
	text = text.replace('Explore the Universe: Random APOD Generator','')
	text = text.replace('Follow APOD on: Facebook,  Google Plus,  Instagram, or Twitter','')
	
	# GET TITLE
	title = (json['title'])

	# SET CONTENT
	content = (date, title, text)

	# IF path DOES NOT EXISTS, CREATE IT
	if not os.path.exists(path):
		os.makedirs(path)

	# CONSTRUCT PATHS VARS
	(savein, saveout) = setpaths(path, imageurl, False)

	# DOWNLOAD IMAGE TO FS
	getimage(imageurl, savein)

	# MAKE AND SAVE IMAGE, IF POSSIBLE
	# RETURNS PATH TO NEW WALLPAPER
	wallpaper = setimage(savein, saveout, getscreensize(), content, style)

	# SET IMAGE AS WALLPAPER
	setwallpaper(wallpaper)

	# NOTIFICATION ABOUT DESKTOP CHANGE
	notify(
		title.replace("'", ""),
		'Boldly go where only aliens have gone before',
		'Background image has been set.',
		'success'
		)

else:
	
	# NOTIFICATION ABOUT FAILURE
	notify(
		'Space, the final frontier!',
		'Apparently, there is no new image today.',
		'Try investing in space travel or something.',
		'error'
		)