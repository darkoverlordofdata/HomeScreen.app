#!/usr/bin/env sh

mkdir -p ${HOME}/Pictures/HomeScreen
convert ${HOME}/GitHub/HomeScreen.app/Resources/themes/wallpaper.authorize.jpg -resize 1368x768 ${HOME}/Pictures/HomeScreen/bg.jpg
convert ${HOME}/Pictures/HomeScreen/bg.jpg -crop 430x170+469+299 ${HOME}/Pictures/HomeScreen/box.jpg
sudo ln -s ${HOME}/Pictures/HomeScreen /usr/local/share/metalock/themes

convert ${HOME}/GitHub/HomeScreen.app/Resources/themes/wallpaper.locked.jpg -resize 1368x768 ${HOME}/Pictures/HomeScreen/bg.jpg

