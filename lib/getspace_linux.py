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

import subprocess

def getscreensize():

	# improve with https://stackoverflow.com/questions/3597965/getting-monitor-resolution-in-python-on-ubuntu/47557813#47557813 ?
	# xdpyinfo  | grep 'dimensions:'
	xrandrquery = subprocess.Popen(['xrandr', '-q'], stdout=subprocess.PIPE)
	
	stdout = xrandrquery.communicate()
	stdout = stdout[0].splitlines()[0]
	stdout = stdout.split(",")[1]

	res = [int(s) for s in stdout.split() if s.isdigit()]

	vw = res[0]
	vh = res[1]

	return (vw, vh)

# def getfontvars(height, explanation):
# 	(missing)

# def setwallpaper(path):

# 	(missing)
	
	# http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
	# http://stackoverflow.com/questions/32264960/how-to-use-change-desktop-wallpaper-using-python-in-ubuntu-14-04-with-unity
	# http://askubuntu.com/questions/85162/how-can-i-change-the-wallpaper-using-a-python-script

	# https://gist.github.com/mtrovo/1110370
	#!/usr/bin/env python
	#-*- coding:utf-8 -*-

	# import commands
	# import os.path
	# from sys import argv

	# def set_gnome_wallpaper(file_path):
	#     command = "gconftool-2 --set \
	#             /desktop/gnome/background/picture_filename \
	#             --type string '%s'" % file_path
	#     status, output = commands.getstatusoutput(command)
	#     return status



	# if __name__ == '__main__':
	#     if len(argv) <= 1:
	#         print "usage: %s img_path" % argv[0]
	#     else:
	#         img_path = os.path.abspath(argv[1])
	#         if not set_gnome_wallpaper(img_path):
	#             print "Wallpaper changed with success."
	#         else:
	#             print "An error ocurred while setting a new wallpaper."