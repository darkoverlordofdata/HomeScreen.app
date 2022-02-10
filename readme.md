# homescreen.app

coordinate login, wallpaper and lock screen into a theme.

## Requirements
* Image Magick 
* Metalock 
* CMake
```
sudo pkg install cmake ImageMagick7 metalock
```


## Install
Copy to /Applications/AutoStart

or

cd /Applications/AutostartImageMagick7
git clone https://github.com/darkoverlordofdata/HomeScreen.app.git

## Features

* select screen lock - ( metalock, catlock, etc. )
* set slim theme per screen lock :
* * /usr/local/share/slim/themes/metalock
* * /usr/local/share/slim/themes/catlock
* download daily wallpaper - ( bing, etc. )
* generate assets for selected screenlock
* generate assets for slim theme


/Applications/Autostart/HomeScreen.app/catlock -t wallpaper -p 420420

## To use Metalock:
### metalock onetime:
sudo ln -s /Applications/Autostart/HomeScreen.app/Resources/themes/WallPaper /usr/local/share/metalock/themes/WallPaper
### metalock daily:
convert /Applications/Autostart/HomeScreen.app/Resources/themes/wallpaper.locked.jpg -resize 1368x768 /Applications/Autostart/HomeScreen.app/Resources/themes/WallPaper/bg.jpg

convert /Applications/Autostart/HomeScreen.app/Resources/themes/WallPaper/bg.jpg -crop 430x170+469+299 /Applications/Autostart/HomeScreen.app/Resources/themes/WallPaper/box.jpg

## To use Catlock:
### catlock onetime
requires the developer image to be installed

cd /Applications/Autostart/HomeScreen.app
./configure
cd build
make

run /Applications/Autostart/HomeScreen.app/catlock -t wallpaper -p 420420
### catlock daily
run the showDownload proc in HomeScreen

## ToDo:
* automate onetime and daily procedures above, add to HomeScreen
* add slimlock
* add to catlock: --timezone -z flag to adjust time zone
* add to catlock: display the wallpaper description text on the top of the screen
* integrate avatar.png or ~/.iface into authorize screen


/Applications/Autostart/HomeScreen.app/catlock -t wallpaper -p 420420

cron:

0 */6 * * * com.github.darkoverlordofdata.badabing --update >/dev/null 2>&1

