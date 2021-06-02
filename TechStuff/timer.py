# -*- coding: utf-8 -*-

import threading
from datetime import datetime, timedelta
from time import sleep

import TechStuff.Worker
import TechStuff.database as db
import TechStuff.wallpaperHandler as wh
import startWidgets


class Reminder(threading.Thread):

    def __init__(self, workdone):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.workdone = workdone
        self.time = datetime.fromisocalendar(2000, 1, 1)

    def run(self):
        """Запуск потока"""
        # бесконечный цикл вайл ворк
        while not self.workdone.is_set():
            print('time check!')
            if not startWidgets.get_reg('WallPaper').endswith('TechStuff\\newWallpaper.jpg'):
                wh.Wallpaper.copy(copyTo='TechStuff', fileName='oldWallpaper.jpg')
                worker = TechStuff.Worker.Worker()
                worker.start()
                self.time = datetime.now()
            now = datetime.now()
            dt = now - self.time
            timeoffset = int(db.ConfigDataBase.get('time')[0])
            if dt > timedelta(minutes=timeoffset):
                worker = TechStuff.Worker.Worker()
                worker.start()
                self.time = datetime.now()
            sleep(15)
