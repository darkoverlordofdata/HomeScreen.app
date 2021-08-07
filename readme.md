# homescreen.app

coordinate login, wallpaper and lock screen into a theme.

* select screen lock - ( metalock, catlock, etc. )
* set slim theme per screen lock :
* * /usr/local/share/slim/themes/metalock
* * /usr/local/share/slim/themes/catlock
* download daily wallpaper - ( bing, etc. )
* generate assets for selected screenlock
* generate assets for slim theme


## CatLock
```
versions:
1. kitty-cat-lock written in C 
2. catlock written in Vala - deprecated?
3. catlock.py - QT doesn't make the cut. It's a good reference version for desired ui.
4. tbd:
4.1 catlock re-done in c++ as slimlock variant?
4.2 kitty-cat-lock upgrade?
```


## To Be Automated:

### one time
mkdir -p /home/darko/Pictures/HomeScreen
sudo ln -s /home/darko/Pictures/HomeScreen /usr/local/share/metalock/themes
sudo ln -s /home/darko/Pictures/HomeScreen/bg.jpg /usr/local/share/slim/themes/HomeScreen/background.jpg

### daily
convert /home/darko/GitHub/HomeScreen.app/Resources/themes/wallpaper.authorize.jpg -resize 1368x768 /home/darko/Pictures/HomeScreen/bg.jpg

convert /home/darko/Pictures/HomeScreen/bg.jpg -crop 430x170+469+299 /home/darko/Pictures/HomeScreen/box.jpg

convert /home/darko/GitHub/HomeScreen.app/Resources/themes/wallpaper.locked.jpg -resize 1368x768 /home/darko/Pictures/HomeScreen/bg.jpg


