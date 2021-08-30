# -*- coding: utf-8 -*-

import threading
from datetime import datetime, timedelta
from time import sleep

import TechStuff.Worker
import TechStuff.database as db
import TechStuff.wallpaperHandler as wh
import startWidgets


class TimeKeeper(threading.Thread):

    def __init__(self, workdone, needrefresh):
        """Инициализация потока"""
        super(TimeKeeper, self).__init__()
        self.workdone = workdone
        self.needrefresh = needrefresh
        self.time = datetime.fromisocalendar(2000, 1, 1)

        self.browser = TechStuff.Worker.createBrowser()

    def run(self):
        """Запуск потока"""
        while not self.workdone.is_set():

            if not startWidgets.get_reg('WallPaper').endswith('TechStuff\\files\\newWallpaper.jpg'):
                wh.Wallpaper.copy(copyTo='TechStuff/files', fileName='oldWallpaper.jpg')
                self.startworker()

            now = datetime.now()
            dt = now - self.time
            timeoffset = int(db.ConfigDataBase.get('time')[0])

            if dt > timedelta(minutes=timeoffset) or self.needrefresh.is_set():
                self.startworker()

            sleep(15)

    def startworker(self):
        self.needrefresh.clear()
        worker = TechStuff.Worker.Worker(self.browser)
        worker.start()
        self.time = datetime.now()
