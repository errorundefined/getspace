# ubuntu version

# - needs font definitions
# - needs screensize function
# - neeeds desktop background function
# - needs os specific notifications

# - should be module:

# 	function checking for osx / linux? and conditionally including the above depending on enviorenment?

# http://askubuntu.com/questions/108764/how-do-i-send-text-messages-to-the-notification-bubbles
# http://askubuntu.com/questions/187022/how-can-i-send-a-custom-desktop-notification

# http://stackoverflow.com/questions/32264960/how-to-use-change-desktop-wallpaper-using-python-in-ubuntu-14-04-with-unity
# http://stackoverflow.com/questions/8220108/how-do-i-check-the-operating-system-in-python
# http://askubuntu.com/questions/85162/how-can-i-change-the-wallpaper-using-a-python-script

# https://gist.github.com/mtrovo/1110370
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import commands
import os.path
from sys import argv

def set_gnome_wallpaper(file_path):
    command = "gconftool-2 --set \
            /desktop/gnome/background/picture_filename \
            --type string '%s'" % file_path
    status, output = commands.getstatusoutput(command)
    return status



if __name__ == '__main__':
    if len(argv) <= 1:
        print "usage: %s img_path" % argv[0]
    else:
        img_path = os.path.abspath(argv[1])
        if not set_gnome_wallpaper(img_path):
            print "Wallpaper changed with success."
        else:
            print "An error ocurred while setting a new wallpaper."