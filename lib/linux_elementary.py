#!/usr/bin/env python

import subprocess

# ELEMENTARY FONT DEFINITION VARIABLES
def getfontvars(height, explanation):

	from PIL import ImageFont
	from math import floor
	import textwrap

	# SET SIZING VARS
	fsizehead = int(floor(height / 45))
	fsizetext = int(floor(height / 55))
	wrapped = textwrap.fill(explanation, 50)
	# SET FONT VARS
	headfont = ImageFont.truetype('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-ExtraBold.ttf',fsizehead)
	textfont = ImageFont.truetype('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-Light.ttf',fsizetext)

	return (fsizehead, fsizetext, wrapped, headfont, textfont)

# ELEMENTARY SET WALLPAPER

# Elementary OS creates a copy of the images set by the user in:
# ~/.local/share/backgrounds/
# 
# PITFALL 1
# Elementary OS does not overwrite an image there ones created –
# so for debugging purposes you may have to delete the picture
# there (instead of in GetSpace's image storage folder)
# 
# PITFALL 2
# This may also be a problem for multi display setups!

def setwallpaper(path):

	subprocess.call(['set-wallpaper', path])