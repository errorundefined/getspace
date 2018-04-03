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

def getuserconsent(message, title):

	from sys import platform as os_type

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