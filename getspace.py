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
url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY' # &date=2018-03-18' # for testing

# GET JSON DATA
json = getjson(url)

##################################
# CHECK IF MEDIA EXISTS
##################################

has_media = 'media_type' in json

if not has_media:
	has_msg = 'msg' in json

	print('Switching to yesterday.')

	if has_msg:
		msg = (json['msg'])
		split = msg.split('No data available for date: ', 1)
		date = split[1]
		date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
		date_time_obj_yesterday = date_time_obj - datetime.timedelta(days=1)

		yesterday = date_time_obj_yesterday.strftime('%Y-%m-%d')

		url = base + '&date=' + yesterday
		json = getjson(url)

##################################
# START LOGIC SPECIFIC TO GETSPACE
##################################
media_type = (json['media_type'])

##################################
# IF VIDEO IS AVAILABLE
##################################
if media_type == 'video':

	from lib.lib_link import openurl

	openurl(
		url = (json['url']),
		question=(
			'There is an APOD video today - do you want to see it now?',
			'Getspace has the ultimate question to the universe!'
			),
		notify_opened=(
			'Space traveling now..',
			'There is an APOD video today.',
			'Getspace opened the video link in your browser.',
			'success'
			),
		notify_copied=(
			'Space traveling now..',
			'There is an APOD video today.',
			'Getspace copied the video link to the clipboard.',
			'success'
			)
		)

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
	# text = (json['explanation']).encode('utf-8')
	text = text.replace('  ',' ')
	text = text.replace('--','-')
	# text = text.replace(' - ',' -- ').decode('utf-8')
	# text = text.replace('--',u'\u2E3A')

	text = text.replace('Explore the Universe: Random APOD Generator','')
	text = text.replace('Almost Hyperspace: Random APOD Generator','')
	text = text.replace('Portal Universe: Random APOD Generator','')

	split = text.split('Follow APOD on: ', 1)
	text = split[0]

	split = text.split('Follow APOD in English on: ', 1)
	text = split[0]

	split = text.split('Get the latest from NASA: ', 1)
	text = split[0]

	split = text.split(' Gallery: Notable images', 1)
	text = split[0]
	
	split = text.split(' Notable Images ', 1)
	text = split[0]

	split = text.split(' Notable images ', 1)
	text = split[0]

	split = text.split(' Today watch: ', 1)
	text = split[0]

	split = text.split(' Watch: ', 1)
	text = split[0]

	split = text.split('Notable APOD Submissions:', 1)
	text = split[0]

	split = text.split('Moon Occults Mars:', 1)
	text = split[0]

	split = text.split('Comet NEOWISE Images: ', 1)
	text = split[0]

	text = text.replace('Notable images submitted to APOD','Notable images submitted to APOD are available via their website.')
	text = text.replace('Mars 2020 Launch: photos from planet Earth','')
	text = text.replace('Astrophysicists: Browse 2,200+ codes in the Astrophysics Source Code Library','')
	text = text.replace('Teachers & Students: Ideas for utilizing APOD in the classroom.','')
	text = text.replace('Experts Debate: How will humanity first discover extraterrestrial life?','')



	split = text.split('An APOD Described on TikTok:', 1)
	text = split[0]
	
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