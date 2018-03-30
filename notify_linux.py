#!/usr/bin/env python

import subprocess

def notify(title, subtitle, text, kind):

	# CHECK FOR COMMON NOTIFICATION SERVERS
	
	# SET notifysrv TO FALSE
	notifysrv = False

	# CHECK FOR NOTIFY-SEND
	if not notifysrv:
		try:
			subprocess.call(['notify-send'])
		except OSError as e:
			if e.errno == os.errno.ENOENT:
				pass
		else:
			notifysrv = 'notify-send'

	# CHECK FOR KDIALOG
	if not notifysrv:
		try:
			subprocess.call(['kdialog'])
		except OSError as e:
			if e.errno == os.errno.ENOENT:
				print 'No compatible notification server found.'
		else:
			notifysrv = 'kdialog'

	# PREPARE VARS WITH DOUBLE TICKS


	# SEND A NOTIFICATION TO THE notifysrv FOUND
	# PREPARE FOR AND SENT TO notify-send
	if notifysrv == 'notify-send':

		if kind == 'error':
			urgency = 'critical'
		else:
			urgency = 'normal'

		# or subprocess.Popen?
		subprocess.call(['notify-send', '-u', urgency, '-t', '5000', title, text])

	# OR PREPARE FOR AND SENT TO kdialog
	elif notifysrv == 'kdialog':

		# or subprocess.Popen?
		subprocess.call(['kdialog', '--passivepopup', '--title', title, text, 5])