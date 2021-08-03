# homescreen.app

coordinated wallpaper with lock screen.

initialy downloading only DailyBing wallpaper, homescreen then uses metalock or catlock, formatting the wallpaper appropriately.


mkdir /home/darko/Pictures
mkdir /home/darko/Pictures/HomeScreen
convert /home/darko/GitHub/HomeScreen.app/Resources/themes/wallpaper.authorize.jpg -resize 1368x768 /home/darko/Pictures/HomeScreen/bg.jpg
convert /home/darko/Pictures/HomeScreen/bg.jpg -crop 430x170+469+299 /home/darko/Pictures/HomeScreen/box.jpg
sudo ln -s /home/darko/Pictures/HomeScreen /usr/local/share/metalock/themes

convert /home/darko/GitHub/HomeScreen.app/Resources/themes/wallpaper.locked.jpg -resize 1368x768 /home/darko/Pictures/HomeScreen/bg.jpg

============
convert -size 430x170 xc:none -draw "roundrectangle 0,0,430,170,15,15" mask.png
convert /home/darko/Pictures/BadaBing/box.jpg -matte mask.png \
  -compose DstIn -composite picture_with_rounded_corners.png


convert /home/darko/Pictures/BadaBing/box.jpg -matte mask.png \
  -compose DstIn -composite /home/darko/Pictures/BadaBing/box.jpg
=============

convert /home/darko/Pictures/BadaBing/box.jpg -alpha set -virtual-pixel transparent -channel A -blur 0x8  -threshold 50% +channel /home/darko/Pictures/BadaBing/box.png