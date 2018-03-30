#!/usr/bin/env python

import os
import subprocess

def dosetbackground(path):

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

def getscreensize():

	# add stuff
	# http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment

def getfontvars(height, explanation):

	from PIL import ImageFont
	from math import floor
	import textwrap

	# SET SIZING VARS
	fsizehead = int(floor(height / 36))
	fsizetext = int(floor(height / 65))
	wrapped = textwrap.fill(explanation, 100)
	# SET FONT VARS
	headfont = ImageFont.truetype("/Library/Fonts/Futura.ttc",fsizehead,index=2)
	textfont = ImageFont.truetype("/System/Library/Fonts/Avenir.ttc",fsizetext)