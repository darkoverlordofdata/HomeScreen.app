#!/usr/bin/env python3

import os
import sys
import subprocess

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QProcess, QObject


LOCAL = os.path.dirname(os.path.abspath(__file__))

class TrayIcon(QSystemTrayIcon):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activated.connect(self.showMenuOnTrigger)

    def showMenuOnTrigger(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QCursor.pos())

        
class WallpaperMenu(QObject):

    def __init__(self, width, height):

        super().__init__()


        icon = QIcon(f'{LOCAL}/Wallpaper.png')
 
        self.width = width
        self.height = height
        # self.tray = QSystemTrayIcon()
        self.tray = TrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.menu = QMenu()
        
        self.tray.setContextMenu(self.menu)
        
        self.actions = []
        self.sliderWindow = None
        
        self.refreshMenu()

            
    def onClicked(self, reason):
        self.refreshMenu()

    def refreshMenu(self):
        self.actions = []
        self.menu.clear()
        self.menu.addSeparator()

        # Gallery: display the image cache as thumbnails, select one
        action = QAction("Gallery")
        action.triggered.connect(self.doGallery)
        self.actions.append(action)
        self.menu.addAction(action)

        # Initialize: create the autostart desktop file
        action = QAction("Initialize")
        action.triggered.connect(self.doInitialize)
        self.actions.append(action)
        self.menu.addAction(action)

        # Download: imediately download the current image
        action = QAction("Download")
        action.triggered.connect(self.doDownload)
        self.actions.append(action)
        self.menu.addAction(action)

        # Schedule: restart the schedule if it stopped
        action = QAction("Schedule")
        action.triggered.connect(self.doScheduler)
        self.actions.append(action)
        self.menu.addAction(action)

        # About: display the about dialog
        action = QAction("About")
        action.triggered.connect(self.doAbout)
        self.actions.append(action)
        self.menu.addAction(action)

        # Exit: quit this program
        self.menu.addSeparator()
        action = QAction("Quit")
        action.triggered.connect(self.exit)
        self.actions.append(action)
        self.menu.addAction(action)

    def exit(self, widget):
        sys.exit()

    # show cache contents
    def doGallery(self):
        subprocess.Popen(["python3", f'{LOCAL}/gallery.py', "--time", "01:01"])          
        

    # set preferences
    def doInitialize(self):
        # create /home/darko/.config/autostart/Wallpaper.desktop
        # run download immediately
        # kill & restart scheduler
        pass


    # download latest image cache
    def doDownload(self):
        subprocess.Popen(["python3", f'{LOCAL}/download.py'])          


    # start the download scheduler
    def doScheduler(self):
        # TODO: prompt for starting time
        subprocess.Popen(["python3", f'{LOCAL}/scheduler.py', "--time", "01:01"])          

    def doAbout(self):
        print("doDialog")
        msg = QMessageBox()
        msg.setWindowTitle("Wallpaper")
        msg.setIconPixmap(QPixmap(f'{LOCAL}/Wallpaper.png').scaledToWidth(64, Qt.SmoothTransformation))
        candidates = ["COPYRIGHT", "COPYING", "LICENSE", "license.md"]
        for candidate in candidates:
            if os.path.exists(LOCAL + "/" + candidate):
                with open(LOCAL + "/" + candidate, 'r') as file:
                    data = file.read()
                msg.setDetailedText(data)
        msg.setText("<h3>Wallpaper</h3>")
        msg.setInformativeText("Download your favorite daily desktop images for your wallpaper and lock screen.")
        msg.exec()


if __name__ == "__main__":

    # Simple singleton:
    # Ensure that only one instance of this application is running by trying to kill the other ones
    # p = QProcess()
    # p.setProgram("pkill")
    # p.setArguments(["-f", os.path.abspath(__file__)])
    # cmd = p.program() + " " + " ".join(p.arguments())
    # print(cmd)
    # p.start()
    # p.waitForFinished()

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()

    # app.setQuitOnLastWindowClosed(False)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    VM = WallpaperMenu(width, height)
    app.exec_()
