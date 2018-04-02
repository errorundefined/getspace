#!/usr/bin/env python

from sys import platform as os_type

def getuserconsent(message, title):

	if os_type == 'darwin':

		import subprocess

		applescript = '''
		set consentGiven to true
		try
			set anAlert to "{}"
			display dialog anAlert with title "{}"
		on error number -128
			set consentGiven to false
		end try'''.format(message, title)

		process = subprocess.Popen(
			['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

		stdout = process.communicate(applescript)

		if 'OK' in stdout[0]:

			consent = True

		else:

			consent = False

	elif os_type in ['linux', 'linux2']:

		from PyZenity import Question

		consent=Question(message)

	else:

		raise Exception('Platform not supported')

	if consent:

		return True

	else:

		return False

def setclipboard(toclipboard):

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