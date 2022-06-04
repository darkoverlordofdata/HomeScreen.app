# Wallpaper.app

### Work in progress ### 
coordinate login, wallpaper and lock screen into a theme.
## Install

### helloSystem
cd /Applications/AutoStart
git clone https://github.com/darkoverlordofdata/Wallpaper.app.git

### Debian Bullseye

cd .local/share
git clone https://github.com/darkoverlordofdata/Wallpaper.app.git

## Features

* download daily wallpaper - ( bing, etc. )


/Applications/Autostart/Wallpaper.app/Resources/catlock.py -p 420420

.local/share/Wallpaper.app/Resources/catlock.py -p 420420



Traceback (most recent call last):
  File "/home/darko/.local/share/Wallpaper.app/Resources/download.py", line 107, in <module>
    subprocess.call(cd_script)
NameError: name 'cd_script' is not defined
