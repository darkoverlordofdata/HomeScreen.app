#!/usr/bin/env python3
import os
import sys
import time
import getopt
import schedule
import threading
import subprocess
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QObject
from PyQt5.QtDBus import QDBusConnection

"""
Scheduler takes the place of cron. 

    Runs daily at 01:01 am
    check to fire every 60 sec
"""


LOCAL = os.path.dirname(os.path.abspath(__file__))

"""
Poxy objecct wraps the downloaded flag
"""
class WallpaperProxy(QObject):

    def __init__(self):
        super().__init__()  
        self.downloadFlag = False

    @pyqtSlot(str, result=bool)
    def downloaded(self, arg):
        ret = self.downloadFlag
        self.downloadFlag = False
        return ret 


def run_download(proxy):
    """
    Run process and return immediately
    """
    proxy.downloadFlag = True
    subprocess.Popen(["python3", f'{LOCAL}/download.py'])          

def run_continuously():
    """
    Start the scheduling thread
    """
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(60)
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

"""
Schedule

schedule.py
"""
if __name__ == '__main__':
    usage = """Usage:
sheduler [OPTION?]

Help Options:
-h, --help           Show help options

Application Options:
--time               time to start
"""
    time_of_day= "01:01"            # default run time

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hot:", ["help", "time=", "once"])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(usage)
            sys.exit()
        elif opt in ["-t", "--time"]:
            time_of_day = arg
        elif opt in ["-o", "--once"]:
            time_of_day = arg

    print("app")
    app = QCoreApplication(sys.argv)

    print("QDBusConnection..isConnected")
    if not QDBusConnection.sessionBus().isConnected():
        print("Cannot connect to the D-Bus session bus.\n"
                "To start it, run:\n"
                "\teval `dbus-launch --auto-syntax`\n");
        sys.exit(1)

    print("QDBusConnection..registerService")
    if not QDBusConnection.sessionBus().registerService('com.darkoverlordofdata.wallpaper.downloaded'):
        print("%s\n" % QDBusConnection.sessionBus().lastError().message())
        sys.exit(1)

    print("WallpaperProxy")
    proxy = WallpaperProxy()
    print("QDBusConnection..registerService")
    QDBusConnection.sessionBus().registerObject('/', proxy,
            QDBusConnection.ExportAllSlots)

    print("schedule")
    schedule.every().day.at(time_of_day).do(run_download, proxy=proxy)
    print("run_continuously")
    run_continuously()
    print("app.exec_")
    sys.exit(app.exec_())

