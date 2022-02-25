#!/usr/bin/env python3
"""Tested by Cat

re-write of catlock, using PyQt5

Screen lock program using assets generated by badabing
 
retain name catlock? Balthazar is still Test Kitty #1. 
I can't use it myself if it can't protect from my cat!


"""

import os, sys, getopt, getpass, pwd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QShortcut
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator, QFont, QImage, QKeySequence
from PyQt5.QtCore import Qt, pyqtSlot, QRegExp, QTimer, QTime, QDateTime

class CatLock(QWidget):

    def __init__(self, sysname, pin, fontFamily, tz, width, height):
        """
        CatLock application
        """
        # Create widget
        super().__init__()  

        self.lockedFlag = True
        self.counter = 0
        self.eol = 0

        # self.installEventFilter(self)

        self.setWindowFlags(
                              Qt.WindowStaysOnTopHint       # cover eveything else
                            | Qt.FramelessWindowHint        # no border
                            | Qt.X11BypassWindowManagerHint # displays on top of panels
                            | Qt.Popup                      # recapture keyboard input fom menu
                            )

        # self.msgSc = QShortcut(QKeySequence('Ctrl+SPACE'), self)
        # self.msgSc.activated.connect(lambda : QMessageBox.information(self,
        #             'Message', 'Ctrl + M initiated'))        
        self.activateWindow()
        self.raise_()
        self.grabKeyboard()
        self.grabMouse()
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height
        self.sysname = sysname
        self.count = 0
        self.pin = pin
        self.fontFamily = fontFamily
        self.tz = tz
        self.full_name = pwd.getpwuid(os.getuid()).pw_gecos
        if self.full_name == ",,,":
            self.full_name = pwd.getpwuid(os.getuid()).pw_name


        local = os.path.dirname(os.path.abspath(__file__))

        with open(local + '/Resources/themes/wallpaper.description') as f:
            self.title = f.readline()
            tmp = f.readline()
            self.info = tmp.split("(")[0]
            self.copyright = tmp.split("(")[1]

        self.authorize = QPixmap(local + '/Resources/themes/wallpaper.authorize.jpg')
        self.locked = QPixmap(local + '/Resources/themes/wallpaper.locked.jpg')

        self.setGeometry(self.left, self.top, self.width, self.height)

        home = os.getenv('HOME')
        if os.path.exists(f'/{home}/.iface'):
            self.avatar = QPixmap(f'{home}/.iface')
        else:
            self.avatar = QPixmap(local + '/Resources/avatar.png')
    
        fnt_60 = QFont(self.fontFamily, 60, QFont.Normal)
        fnt_30 = QFont(self.fontFamily, 30, QFont.Normal)
        fnt_20 = QFont(self.fontFamily, 20, QFont.Normal)
        fnt_12 = QFont(self.fontFamily, 12, QFont.Normal)
        fnt_10 = QFont(self.fontFamily, 10, QFont.Normal)


        self.background = QLabel(self)
        self.background.setPixmap(self.locked)

        self.userpic = QLabel(self)
        self.userpic.setPixmap(self.avatar)
        self.userpic.move(int(self.width*.5 - self.userpic.width()*.5), int(self.height*.35))
        self.userpic.setVisible(False)

        self.username = QLabel(self)
        self.username.setFont(fnt_20)
        self.username.setText(self.full_name)
        self.username.move(int((self.width*.5)-(len(self.full_name)*.5)-(len(self.full_name)*6)), int(self.height*.666-80))
        self.username.setStyleSheet("color: white")
        self.username.setVisible(False)

        self.textbox = QLineEdit(self)
        self.textbox.setEchoMode(QLineEdit.Password)
        
        # https://stackoverflow.com/questions/1247762/regex-for-all-printable-characters
        # reg_ex = QRegExp("\P{Cc}\P{Cn}\P{Cs}")
        # input_validator = QRegExpValidator(reg_ex, self.textbox)
        # self.textbox.setValidator(input_validator)
        self.textbox.move(int((self.width*.5)-140), int(self.height*.666))
        self.textbox.resize(280,40)
        self.textbox.setVisible(False)

        self.instructions = QLabel(self)
        self.instructions.setFont(fnt_10)
        self.instructions.setText("Enter PIN")
        self.instructions.move(int(self.width*.5)-30, int(self.height*.666+60))
        self.instructions.setVisible(False)
        self.instructions.setStyleSheet("color: white")

        self.titlebox = QLabel(self)
        self.titlebox.setFont(fnt_20)
        self.titlebox.setText(self.title)
        self.titlebox.move(60, 40)
        self.titlebox.setStyleSheet("color: white")
        self.titlebox.setFocusPolicy(Qt.ClickFocus | Qt.TabFocus | Qt.NoFocus)

        self.infobox = QLabel(self)
        self.infobox.setFont(fnt_12)
        self.infobox.setText(self.info)
        self.infobox.move(60, 80)
        self.infobox.setStyleSheet("color: white")

        self.copybox = QLabel(self)
        self.copybox.setFont(fnt_10)
        self.copybox.setText(self.copyright[:-1])
        self.copybox.move(60, 110)
        self.copybox.setStyleSheet("color: white")

        #
        # 1366 x 768
        # 530, 650
        # 1920 x 1080
        # 800, 925

        # 75%, 85%
        # 

        
        # row1 = int(self.height * 0.70)
        # row2 = int(self.height * 0.85)


        self.clock = QLabel(self)
        self.clock.setFont(fnt_60)
        self.clock.move(60, int(self.height * 0.70))
        self.clock.setStyleSheet("color: white")

        self.calendar = QLabel(self)        
        self.calendar.setFont(fnt_30)
        self.calendar.move(60, int(self.height * 0.85))
        self.calendar.setStyleSheet("color: white")

        self.showTime()
        self.clock.show()
        self.calendar.show()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second
        self.show()

    def eventFilter(self, source, event):
        print(source)
        print(event)
        return super(CatLock, self).eventFilter(source, event)

    def showTime(self):
        currentTime = QDateTime.currentDateTime()
        adj = 60*60*(self.tz) # 'cause i'm stuck in EDT
        currentTime = currentTime.addSecs(adj)

        self.clock.setText(currentTime.toString('h:mm a'))
        self.calendar.setText(currentTime.toString('dddd, MMMM d'))

        # self.eol += 1
        # if self.eol > 10:
        #     self.exitLock()

        # check if we're ready to return to lock screen
        if self.lockedFlag == False:
            self.counter += 1
            if self.counter > 30:
                self.lockedFlag = True
                self.background.setPixmap(self.locked)
                self.textbox.setText("")
                self.textbox.setVisible(False)
                self.username.setVisible(False)
                self.userpic.setVisible(False)
                self.instructions.setVisible(False)

                self.titlebox.setVisible(True)
                self.infobox.setVisible(True)
                self.copybox.setVisible(True)
                self.clock.setVisible(True)
                self.calendar.setVisible(True)  

    def keyPressEvent(self, event):
        """
        decode the keypress:

            Key_Escape
                kills input, relock screen

            Key_Return
                force check of valid pin
                clear input buffer

            Key_Backspace
                delete last char

        """
        if event.key() == Qt.Key_Escape:
            # self.exitLock()

            self.background.setPixmap(self.locked)
            self.textbox.setText("")
            self.textbox.setVisible(False)
            self.username.setVisible(False)
            self.userpic.setVisible(False)
            self.instructions.setVisible(False)

            self.titlebox.setVisible(True)
            self.infobox.setVisible(True)
            self.copybox.setVisible(True)
            self.clock.setVisible(True)
            self.calendar.setVisible(True)  

        elif event.key() == Qt.Key_Return:
            if self.textbox.text() == self.pin:
                self.exitLock()
            self.textbox.clear()

        elif event.key() == Qt.Key_Backspace:
            if self.textbox.hasFocus():
                self.textbox.backspace()
            else:
                self.textbox.setText(self.textbox.text()[:-1])

        else:
            self.lockedFlag = False
            self.counter = 0 # reset timer to go back to lock screen

            if self.textbox.isHidden():
                self.titlebox.setVisible(False)
                self.infobox.setVisible(False)
                self.copybox.setVisible(False)
                self.clock.setVisible(False)
                self.calendar.setVisible(False)
                  
                self.background.setPixmap(self.authorize)
                self.username.setVisible(True)
                self.textbox.setVisible(True)
                self.userpic.setVisible(True)
                self.instructions.setVisible(True)
                self.textbox.setText(event.text())

                # pm = self.textbox.grab()
                # pm.save("/home/darko/widget.png")


            else:
                if self.textbox.hasFocus():
                    if self.textbox.text() == self.pin:
                        self.exitLock()
                else:
                    self.textbox.setText(self.textbox.text()+event.text())
                    if self.textbox.text() == self.pin:
                        self.exitLock()

    def exitLock(self):
        """
        exit screen lock
        """
        self.releaseKeyboard()
        self.releaseMouse()
        self.close()
        exit()



if __name__ == '__main__':
    usage = """Usage:
catlock [OPTION?]

Help Options:
-h, --help           Show help options

Application Options:
--pin                lock number
--font               font family
--tz                 time zone correction
"""

    pin = '1234'
    fontFamily = 'Verdana'
    tz = 0

    

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.size()
    width = size.width()
    height = size.height()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                        "hp:f:t:w:h", 
                                        [ 
                                            "help",
                                            "pin=",
                                            "font=",
                                            "tz=" 
                                        ])
    except getopt.GetoptError:  
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(usage)
            sys.exit()
        elif opt in ["-p", "--pin"]:
            pin = arg
        elif opt in ["-f", "--font"]:
            fontFamily = arg
        elif opt in ["-t", "--tz"]:
            tz = int(arg)

    ex = CatLock(os.uname().sysname, pin, fontFamily, tz, width, height)
    sys.exit(app.exec_())
