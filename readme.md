# wallpaper.app

### nb: renamed to Wallpaper.app
 
coordinate wallpaper and lock screen into a theme.

catlock.py is based on my vala catlock code, using pyqt5
Wallpaper is a panel bar app to set up the infastructure.
?This will become a standad app.?

## Install

### helloSystem
Copy to ~Applications

The first time run, ~Applications/Wallpaper.app/Wallpaper will do any setup

After that, use to adjust settings

### Debian Bullseye
copy project to .local/share

copy ./applications to .local/share/applications

#### optional - 
if keybinding is not available

copy alacarte-made.dockitem to /home/pi/.config/plank/dock1/launchers

## Features

* select screen lock - ( metalock, catlock.py, etc. )
* download daily wallpaper - ( bing, etc. ) with chron
* generate assets for selected screenlock
* maintain last 7 days history
* screen lock can cycle thru history and show last weeks worth pictures

### Implementation
* Create Catlock.desktop
* Create Wallpaper.desktop
* Schedule download chron job
* Bind shortcut key
* Execute current download

/usr/bin/python3 /home/darko/.local/share/Wallpaper.app/catlock.py --pin 420420

## pograms

* **schedule.py**     schedule download of pictures
* **download.py**     run 1 download
* **catlock.py**      sceenlock
* **Wallpaper**      Panel Gui 