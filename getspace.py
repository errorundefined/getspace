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
import argparse

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
# PARSE ARGUMENTS
##################################

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--notifications', help='deliver system notifications', action='store_true')
args = parser.parse_args()
if args.notifications:
	print 'notifications turned on'

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

if media_type == 'video' or media_type == 'image':
	video_to_image = False

	##################################
	# IF VIDEO IS AVAILABLE
	##################################
	if media_type == 'video':

		# from lib.lib_link import openurl

		# quit() # !!!!!!

		# openurl(
		# 	url = (json['url']),
		# 	question=(
		# 		'There is an APOD video today - do you want to see it now?',
		# 		'Getspace has the ultimate question to the universe!'
		# 		),
		# 	notify_opened=(
		# 		'Space traveling now..',
		# 		'There is an APOD video today.',
		# 		'Getspace opened the video link in your browser.',
		# 		'success'
		# 		),
		# 	notify_copied=(
		# 		'Space traveling now..',
		# 		'There is an APOD video today.',
		# 		'Getspace copied the video link to the clipboard.',
		# 		'success'
		# 		)
		# 	)

		from urlparse import urlparse, parse_qs

		url = (json['url'])

		if url.startswith(('youtu', 'www')):
			url = 'https://' + url

		query = urlparse(url)

		if 'youtube' in query.hostname:
			if query.path == '/watch':
				youtubeid = parse_qs(query.query)['v'][0]
			elif query.path.startswith(('/embed/', '/v/')):
				youtubeid = query.path.split('/')[2]
		elif 'youtu.be' in query.hostname:
			youtubeid = query.path[1:]

		if youtubeid:
			imageurl = 'https://img.youtube.com/vi/' + youtubeid + '/maxresdefault.jpg'
			video_to_image = True

	##################################
	# IF IMAGE IS AVAILABLE
	##################################
	if media_type == 'image' or video_to_image:

		from lib.lib_image import setpaths, getimage, setimage

		# GET DATE
		date = (json['date'])

		# GET IMAGE URL
		if not video_to_image:
			imageurl = (json['hdurl'])

		# GET AND CLEAN UP TEXT
		text = (json['explanation'])
		# text = (json['explanation']).encode('utf-8')
		text = text.replace('  ',' ')
		text = text.replace('--','-')
		# text = text.replace(' - ',' -- ').decode('utf-8')
		# text = text.replace('--',u'\u2E3A')

		stringdeleters = ['Explore the Universe: Random APOD Generator',
				'Almost Hyperspace: Random APOD Generator',
				'Portal Universe: Random APOD Generator',
				'Mars 2020 Launch: photos from planet Earth',
				'Astrophysicists: Browse 2,200+ codes in the Astrophysics Source Code Library',
				'Teachers & Students: Ideas for utilizing APOD in the classroom.',
				'Experts Debate: How will humanity first discover extraterrestrial life?'
			]
		for string in stringdeleters:
			text = text.replace(string,'')

		stringmarkers = ['Follow APOD on: ',
				'Follow APOD in English on: ',
				'Get the latest from NASA: ',
				' Gallery: Notable images',
				' APOD in world languages: ',
				' APOD Year in Review ',
				' APOD is available ',
				' Notable Images ',
				' Notable images ',
				' Today watch: ',
				' Watch: ',
				'Notable APOD Submissions:',
				'Moon Occults Mars:',
				'Comet NEOWISE Images: ',
				'An APOD Described on TikTok:'
			]
		for string in stringmarkers:
			split = text.split(string, 1)
			text = split[0]

		text = text.replace('Notable images submitted to APOD','Notable images submitted to APOD are available via their website.')
		
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
		if args.notifications:
			notify(
				title.replace("'", ""),
				'Boldly go where only aliens have gone before',
				'Background image has been set.',
				'success'
				)

else:
	
	# NOTIFICATION ABOUT FAILURE
	if args.notifications:
		notify(
			'Space, the final frontier!',
			'Apparently, there is no new image today.',
			'Try investing in space travel or something.',
			'error'
			)