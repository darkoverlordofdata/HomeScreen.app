#!/usr/bin/env python3

# from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QHBoxLayout, QGroupBox, QSlider, QWidget, \
#     QActionGroup, QDesktopWidget, QMessageBox
# from PyQt5.QtGui import QIcon, QPixmap, QCursor, QImage
# from PyQt5.QtCore import Qt, QProcess, QMetaObject, QCoreApplication, QEvent, QObject, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage

import sys
import os
import json
import requests
import dbus
import subprocess
from os.path import exists


LOCAL = os.path.dirname(__file__)

 
# def procDownload():
if __name__ == "__main__":

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()

    response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    image_data = json.loads(response.text)

    image_url = image_data["images"][0]["url"]
    
    urlbase = image_data["images"][0]["urlbase"][11:] # remove /th?id=OHR.
    title = image_data["images"][0]["title"]
    copyright = image_data["images"][0]["copyright"]

    image_url = image_url.split("&")[0]
    full_image_url = "https://www.bing.com" + image_url
    img_data = requests.get(full_image_url).content

    with open(f'{LOCAL}/imagename', 'w') as f:
        f.write(urlbase)

    with open(f'{LOCAL}/gallery/{urlbase}.jpeg', 'wb') as f:
        f.write(img_data)

    with open(f'{LOCAL}/gallery/{urlbase}', 'w') as f:
        f.write(title)
        f.write('\n')
        f.write(copyright)

    # width = 1920 # 1368
    # height = 1080 # 768

    image = QImage(f'{LOCAL}/gallery/{urlbase}.jpeg', 'JPG')
    locked = QPixmap.fromImage(image).scaled(width, height) #, Qt.KeepAspectRatio)

    for i in range(image.height()):
        for k in range(image.width()):
            image.setPixelColor(k, i, image.pixelColor(k,i).darker(160))

    authorize = QPixmap.fromImage(image).scaled(width, height) #, Qt.KeepAspectRatio)

    authorize.save(f'{LOCAL}/themes/wallpaper.authorize.jpg')
    locked.save(f'{LOCAL}/themes/wallpaper.locked.jpg')
    with open(f'{LOCAL}/themes/wallpaper.description', 'w') as f:
        f.write(title)
        f.write('\n')
        f.write(copyright)

    XDG_CURRENT_DESKTOP = os.environ['XDG_CURRENT_DESKTOP']
    print(f'XDG_CURRENT_DESKTOP = {XDG_CURRENT_DESKTOP}')
    print(f'"file://\'{LOCAL}/gallery/{urlbase}.jpeg\'"')

    # helloSystem
    if os.path.exists('/usr/local/bin/launch'): 
        os.system(f'launch Filer --set-wallpaper {LOCAL}/gallery/{urlbase}.jpeg')

    # LXDE
    elif os.path.exists('/usr/bin/pcmanfm'): 
        os.system(f'pcmanfm --set-wallpaper {LOCAL}/gallery/{urlbase}.jpeg')

    # Ubuntu Gnome
    elif os.environ['XDG_CURRENT_DESKTOP'] == 'ubuntu:GNOME':
        os.system(f'dconf write /org/gnome/desktop/background/picture-uri "\'file://{LOCAL}/gallery/{urlbase}.jpeg\'"')

    # Ubuntu Unity
    elif os.environ['XDG_CURRENT_DESKTOP'] == 'Unity':
        os.system(f'dconf write /org/gnome/desktop/background/picture-uri "\'file://{LOCAL}/gallery/{urlbase}.jpeg\'"')

    #Wich Unity? It changes...
    elif os.environ['XDG_CURRENT_DESKTOP'] == 'Unity:Unity7:ubuntu':
        os.system(f'dconf write /org/gnome/desktop/background/picture-uri "\'file://{LOCAL}/gallery/{urlbase}.jpeg\'"')

    # MATE
    elif os.environ['XDG_CURRENT_DESKTOP'] == 'MATE':
        os.system(f'dconf write /org/mate/desktop/background/picture-filename "\'{LOCAL}/gallery/{urlbase}.jpeg\'"')

    # KDE
    elif os.environ['XDG_CURRENT_DESKTOP'] == 'KDE':
        plugin = 'org.kde.image'
        filepath = f'{LOCAL}/gallery/{urlbase}.jpeg'
        filepath = filepath.replace("/./", "/")
        user = os.environ['USER']

        jscript = """
        var allDesktops = desktops();
        print (allDesktops);
        for (i=0;i<allDesktops.length;i++) {
            d = allDesktops[i];
            d.wallpaperPlugin = "%s";
            d.currentConfigGroup = Array("Wallpaper", "%s", "General");
            d.writeConfig("Image", "%s")
        }
        """
        # print(jscript % (plugin, plugin, filepath))

        bus = dbus.SessionBus()
        plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        plasma.evaluateScript(jscript % (plugin, plugin, filepath))

        print( f'/usr/bin/kwriteconfig5 --file /home/{user}/.config/kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image {filepath}' )

        cmd_script = [
            'DISPLAY=:0 ' 
            f'/usr/bin/kwriteconfig5 --file /home/{user}/.config/kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image {filepath}'
        ] 
        subprocess.run(cmd_script,shell=True)

    # Unknown???       
    else:
        print('Desktop not recognized')



