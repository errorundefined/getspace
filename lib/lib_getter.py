#!/usr/bin/env python

# JSON IMPORT WITH FAILSAFE
def getjson(url):

	import json
	import urllib

	jsonstuff = False

	try:
		response = urllib.urlopen(url)

		# LOAD JSON DATA FROM OBJECT
		jsonstuff = json.load(response)

	except IOError, e:

		print 'Using CURL fallback.'

		import subprocess

		process = subprocess.Popen(['curl', url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		response = stdout
		
		# LOAD JSON DATA FROM STRING
		jsonstuff = json.loads(response)

	if not json:
		print 'Failed! JSON could not be downloaded.'
		quit()

	else:
		print 'JSON has been downloaded.'

	return jsonstuff

# DETECTION OF ENVIRONMENT + TEXT FORMATS DEPENDING ON THAT
def getenvironment(scriptname, saveinfolder):

	import os
	from sys import platform as os_type

	# ENV VARIABLE
	home = os.getenv('HOME')

	# CONDITIONALLY SET OS SPECIFIC ENV..
	# ..IF OSX/MACOS:
	if os_type == 'darwin':
		
		# ..SET ENV VARIABEL
		osenvironment = 'macos'

		# ..SET PATH
		path = home + '/Pictures/' + saveinfolder

		# ..SET STYLE
		headstyle = ('/Library/Fonts/Futura.ttc', 2, 36)
		textstyle = ('/System/Library/Fonts/Avenir.ttc', 0, 65)
		text_wraplength = 100

		# ..AND STDOUT.
		print scriptname + ' is running on OSX/macOS'

	# ..IF LINUX:
	elif os_type in ['linux', 'linux2']:

		# ..IMPORT MODULES
		from platform import linux_distribution
		distro = linux_distribution()[0]

		# ..SET PATH
		path = home + saveinfolder # ?? (maybe correct with home = os.path.expanduser('~') ??)

		# ..AND GO INTO DETAILS:
		# ..IF ELEMENTARY OS
		if 'elementary' in distro:

			# ..SET ENV VARIABEL
			osenvironment = 'elementary'

			# ..SET STYLE
			headstyle = ('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-ExtraBold.ttf', 0, 45)
			textstyle = ('/usr/share/fonts/truetype/open-sans-elementary/OpenSans-Light.ttf', 0, 55)
			text_wraplength = 100

			# ..AND STDOUT.
			print scriptname + ' is running as getspace_linux_elementary -- there may be bugs'

		else:			
			# from lib.getspace_linux import notify, getscreensize, getfontvars, setwallpaper
			print scriptname + ' does not yet fully support most linux versions'
			return False
	else:		
		return False

	style = (headstyle, textstyle, text_wraplength)

	return osenvironment, path, style