#!/usr/bin/env python

import os

# OSX NOTIFICATION FUNCTION
def notify(title, subtitle, text, kind):

	if kind == 'success':
		sound = 'Submarine'
	else:
		sound = 'Basso'

	os.system("""
		osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "{}"'
		""".format(text, title, subtitle, sound))

# OSX SCREEN SIZE FUNCTION
def getscreensize():
	import AppKit
	# wrong because in a multi screen setup, it would return the size of the last screen in the array
	for screen in AppKit.NSScreen.screens(): 
		vw = screen.frame().size.width
		vh = screen.frame().size.height
	return (vw, vh)

# OSX FONT DEFINITION VARIABLES
def getfontvars(height, explanation):
	
	from PIL import ImageFont
	from math import floor
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

	return (fsizehead, fsizetext, wrapped, headfont, textfont)


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

# ADD FUNCTION FOR CHANGING ADMIN LOGIN PNG
# dosetbackground(savein)
	# loginimage = '/Library/Caches/com.apple.desktop.admin.png'
	
	# try:
	# 	os.remove(loginimage) # OSX REGENERATES FILE AUTOMATICALLY / or not
	# except OSError:
	# 	pass

	# admin = img.filter(ImageFilter.GaussianBlur(radius=15))
	# admin.save(loginimage)