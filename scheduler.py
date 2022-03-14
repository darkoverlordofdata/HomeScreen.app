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
        opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "time="])
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

    app = QCoreApplication(sys.argv)

    if not QDBusConnection.sessionBus().isConnected():
        sys.stderr.write("Cannot connect to the D-Bus session bus.\n"
                "To start it, run:\n"
                "\teval `dbus-launch --auto-syntax`\n");
        sys.exit(1)

    if not QDBusConnection.sessionBus().registerService('com.darkoverlordofdata.wallpaper.downloaded'):
        sys.stderr.write("%s\n" % QDBusConnection.sessionBus().lastError().message())
        sys.exit(1)

    proxy = WallpaperProxy()
    QDBusConnection.sessionBus().registerObject('/', proxy,
            QDBusConnection.ExportAllSlots)

    schedule.every().day.at(time_of_day).do(run_download, proxy=proxy)
    run_continuously()
    sys.exit(app.exec_())

