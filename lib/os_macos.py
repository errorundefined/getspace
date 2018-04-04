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
import subprocess

# OSX SCREEN SIZE FUNCTION
def getscreensize():

	# import AppKit
	# # wrong because in a multi screen setup, it would return the size of the last screen in the array
	# for screen in AppKit.NSScreen.screens(): 
	# 	vw = screen.frame().size.width
	# 	vh = screen.frame().size.height
	# return (vw, vh)

	# system_profiler SPDisplaysDataType | grep Resolution | grep -oE '[0-9]+' | grep -Eo '[0-9]+$'
	systemprofile = subprocess.Popen(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE)
	stdout = systemprofile.communicate()
	stdout = stdout[0].splitlines()
	for line in stdout:
		if 'Resolution' in line:
			res = [int(s) for s in line.split() if s.isdigit()]
			vw = res[0]
			vh = res[1]
	return (vw, vh)

# OSX SET WALLPAPER
def setwallpaper(path):

	# GET OSX VERSION NUMBER
	import platform
	
	version = platform.mac_ver()

	# SET COMMAND DEPENDING ON OSX VERSION
	if version[0] >= 10.9:
		# AFTER MAVERICKS: SQLITE SOLUTION
		# seems to be working though it uses killall Dock and all desktops have to be created from the first
		# add an  WHERE ROWID='1' ??
		setbackgroundcmd = """
		sqlite3 ~/Library/Application\ Support/Dock/desktoppicture.db "UPDATE data SET value='{}'" && killall Dock
		""".format(path)

	else:
		# BEFORE MAVERICKS: APPLESCRIPT SOLUTION
		setbackgroundcmd = """
		osascript -e 'tell application "System Events"
		set desktopCount to count of desktops
		repeat with desktopNumber from 1 to desktopCount
			tell desktop desktopNumber
				set picture to "{}"
			end tell
		end repeat
		end tell'
		""".format(path)

		# setbackgroundcmd = """
		# osascript -e 'tell application "System Events" to set picture of every desktop to ("{}" as POSIX file as alias)'
		# """.format(path)

	os.popen(setbackgroundcmd)

	print 'Background set.'


# ADD FUNCTION FOR CHANGING ADMIN LOGIN PNG
# setwallpaper(savein)
	# loginimage = '/Library/Caches/com.apple.desktop.admin.png'
	
	# try:
	# 	os.remove(loginimage) # OSX REGENERATES FILE AUTOMATICALLY / or not
	# except OSError:
	# 	pass

	# admin = img.filter(ImageFilter.GaussianBlur(radius=15))
	# admin.save(loginimage)