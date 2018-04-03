def notify(title, subtitle, text, kind):

	import os
	import subprocess
	from sys import platform as os_type

	if os_type == 'darwin':

		# IF YOU DO NOT LIKE SOUNDS WITH YOUR NOTIFICATIONS (DEFAULT)
		os.system("""
			osascript -e 'display notification "{}" with title "{}" subtitle "{}"'
			""".format(text, title, subtitle))

		# IF YOU LIKE SOUNDS WITH YOUR NOTIFICATIONS
		# if kind == 'success':
		# 	sound = 'Submarine'
		# else:
		# 	sound = 'Basso'

		# os.system("""
		# 	osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "{}"'
		# 	""".format(text, title, subtitle, sound))

	elif os_type in ['linux', 'linux2']:

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

	else:

		raise Exception('Platform not supported')