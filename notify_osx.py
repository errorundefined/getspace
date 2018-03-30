#!/usr/bin/env python

import os

def notify(title, subtitle, text, kind):

	if kind == 'success':
		sound = 'Submarine'
	else:
		sound = 'Basso'

	os.system("""
		osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "{}"'
		""".format(text, title, subtitle, sound))