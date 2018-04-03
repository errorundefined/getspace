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

def setclipboard(toclipboard):

	from sys import platform as os_type

	import subprocess

	# https://stackoverflow.com/a/25802742
	if os_type == 'darwin':

		process = subprocess.Popen(
			'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
		
		process.communicate(toclipboard.encode('utf-8'))

	# https://stackoverflow.com/a/7606100
	elif os_type in ['linux', 'linux2']:

		process = subprocess.Popen(
			['xsel', '-bi'], stdin=subprocess.PIPE)

		process.communicate(toclipboard)

	# https://gist.github.com/adam-p/4173174
	elif os_type in ['win32', 'cygwin']:

		process = subprocess.Popen(
			['clip'], stdin=subprocess.PIPE)

		process.communicate(toclipboard)

	else:

		raise Exception('Platform not supported')