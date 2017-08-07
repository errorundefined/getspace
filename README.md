# GetSpace – APOD wallpaper
Change your wallpaper to today's Astronomy Picture of the Day, everyday – along with a brief explanation.

## Todo
- [X] add upscaling (to avoid blurred font rendering)
- [ ] add support for multi display setups

### OSX
- [ ] get ```com.apple.desktop.admin.png``` thing to work

### Linux
- [ ] add ```def dosetbackground(path)```
- [ ] add ```def getscreensize()```
- [ ] add ```def getfontvars(height, explanation)```
- [ ] add cron explanation

## Readme

### Requirements

#### API Key

You sould get an API key as this thing here uses the limited ```DEMO_KEY``` – you can do so for free at ([NASA Open APIs](https://api.nasa.gov/index.html#apply-for-an-api-key)). After that, in line 43 of getspace.py, remove ```DEMO_KEY``` and put your API key after ```https://api.nasa.gov/planetary/apod?api_key=```.

#### Pillow (PIL Fork)

In order to get information on the current APOD image onto your background image, you need to install ([Pillow](https://python-pillow.org/)) if it is not already shipped with your OS. If this is not done, the image (without info) is still being set as the new desktop background.

#### OSX

Most of the times:

```$ sudo easy_install pip```

```$ (sudo) pip install Pillow```

#### Linux

Use native operating system package manager to install PIL/Pillow ([comp. the Pillow Docs](http://pillow.readthedocs.io/en/latest/installation.html#linux-installation)), for example:

```$ apt-get install python-pillow```

```$ zypper install python-Pillow``` (openSUSE)

```$ dnf (or yum) install python-pillow``` (Fedora)

### Scheduling
In order to schedule getspace to do it's thing automatically you've to:

#### OSX

- do ```$ cd /path/to/getspace.py /Users/USERNAME/.bin``` to put the script into you .bin folder
- change the ```USERNAME``` within the "Program" string in ```local.getspace.plist```
- do ```$ cd /path/to/local.getspace.plist ~/Library/LaunchAgents```to add the changed plist into you Library

#### Linux (notes)

```30 12 * * * /path/to/getspace.py``` (alyways 12.30h)

```@reboot /path/to/getspace.py``` (after Reboot, checken, if after hibernate)

([comp. CronHowto on Ubuntu](https://help.ubuntu.com/community/CronHowto))

#### executing by hand

if the above is not (yet) done, you can always run the script manually like so:

```$ python /path/to/getspace.py```

## Authors
[error:undefined design](http://error-undefined.de/)

## License

[MIT](https://opensource.org/licenses/MIT)

It is discouraged to use this script in any project that promotes racism, sexism, homophobia, animal abuse, violence or any other form of hate speech.
