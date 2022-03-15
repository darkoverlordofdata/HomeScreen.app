# Wallpaper.app

coordinate login, wallpaper and lock screen into a theme.
## Install

### helloSystem
Copy to /Applications/AutoStart

### Debian Bullseye
copy to /usr/local/share

cd /Applications/AutostartImageMagick7
git clone https://github.com/darkoverlordofdata/Wallpaper.app.git

## Features

* select screen lock - ( metalock, catlock.py, etc. )
* download daily wallpaper - ( bing, etc. )
* generate assets for selected screenlock


/Applications/Autostart/Wallpaper.app/catlock -t wallpaper -p 420420

## To use Metalock:
### metalock onetime:
sudo ln -s /Applications/Autostart/Wallpaper.app/Resources/themes/WallPaper /usr/local/share/metalock/themes/WallPaper
### metalock daily:
convert /Applications/Autostart/Wallpaper.app/Resources/themes/wallpaper.locked.jpg -resize 1368x768 /Applications/Autostart/Wallpaper.app/Resources/themes/WallPaper/bg.jpg

convert /Applications/Autostart/Wallpaper.app/Resources/themes/WallPaper/bg.jpg -crop 430x170+469+299 /Applications/Autostart/Wallpaper.app/Resources/themes/WallPaper/box.jpg

## To use Catlock:
### catlock onetime
requires the developer image to be installed

cd /Applications/Autostart/Wallpaper.app
./configure
cd build
make

run /Applications/Autostart/Wallpaper.app/catlock -t wallpaper -p 420420

/usr/bin/python3 /home/darko/.local/share/Wallpaper.app/catlock.py -p 420420

sudo ln -s /home/pi/Documents/GitHub/Wallpaper.app/Resources/themes/WallPaper /usr/local/share/metalock/themes/WallPaper


### catlock daily
run the showDownload proc in HomeScreVen 

## ToDo:
* automate onetime and daily procedures above, add to Wallpaper
* add slimlock
* add to catlock: --timezone -z flag to adjust time zone
* add to catlock: display the wallpaper description text on the top of the screen
* integrate avatar.png or ~/.iface into authorize screen


/Applications/Autostart/Wallpaper.app/catlock -t wallpaper -p 420420

cron:

0 */6 * * * com.github.darkoverlordofdata.badabing --update >/dev/null 2>&1

0 */6 * * * /usr/bin/python3 /home/darko/.local/share/Wallpaper.app/download.py >/dev/null 2>&1

/home/pi/Documents/GitHub/Wallpaper.app/build/catlock  -t wallpaper -p 420420

python3 /home/pi/Documents/GitHub/Wallpaper.app/catlock.py --pin 420
