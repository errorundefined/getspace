#!/usr/bin/env python

def openurl(url, question, notify_opened, notify_copied):

	from pynotify.pynotify import notify
	from pyquestion.pyquestion import getuserconsent

	if getuserconsent(*question):

		import webbrowser
		webbrowser.open_new_tab(url)

		notify(*notify_opened)
		print 'Link opened in browser.'

	else:
		
		from pytoclipboard.pytoclipboard import setclipboard
		setclipboard(url)
		
		notify(*notify_copied)
		print 'Link copied to clipboard.'