# getspace – Python script using NASA's Astronomy Picture of the Day API
APOD wallpaper command line client written in Python (it even put's info text on the picture)

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

```$ yum install python-Pillow``` (Fedora)

### Scheduling
In order to schedule getspace to do it's thing automatically you've to:

#### OSX

- put the ```getspace.py``` to ```/Users/USERNAME/.bin/getspace.py```
- change the ```USERNAME``` within the "Program" string in ```local.getspace.plist```
- add the changed ```local.getspace.plist``` into your ```~/Library/LaunchAgents```

#### Linux

```30 12 * * * /path/to/getspace.py``` (alyways 12.30h)
```@reboot /path/to/getspace.py``` (after Reboot, checken, if after hibernate)

([comp. CronHowto on Ubuntu](https://help.ubuntu.com/community/CronHowto))

#### executing by hand

if the above is not (yet) done, you can always run the script manually like so:

```$ python /path/to/getspace.py```

## Todo
- add upscaling (to avoid blurred font rendering)

### OSX
- add support for multi display setups

### Linux
- add ```def dosetbackground(path)```
- add ```def getscreensize()```
- add ```def getfontvars(height, explanation)```

## Authors
[error:undefined design](http://error-undefined.de/)

## License

[MIT](https://opensource.org/licenses/MIT)

It is discouraged to use this plugin in any project that promotes racism, sexism, homophobia, animal abuse, violence or any other form of hate speech.