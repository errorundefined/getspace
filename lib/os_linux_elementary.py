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

# ELEMENTARY SET WALLPAPER

# Elementary OS creates a copy of the images set by the user in:
# ~/.local/share/backgrounds/
# 
# PITFALL 1
# Elementary OS does not overwrite an image there once created -
# so for debugging purposes you may have to delete the picture
# there (instead of in GetSpace's image storage folder)
# 
# PITFALL 2
# This may also be a problem for multi display setups!

def setwallpaper(path):

	subprocess.call(['set-wallpaper', path])

	print 'Background set.'