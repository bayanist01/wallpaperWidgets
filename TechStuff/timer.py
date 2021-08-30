# -*- coding: utf-8 -*-

import threading
from datetime import datetime, timedelta
from time import sleep
from selenium import webdriver

import TechStuff.Worker
import TechStuff.database as db
import TechStuff.wallpaperHandler as wh
import startWidgets


class Reminder(threading.Thread):

    def __init__(self, workdone, needrefresh):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.workdone = workdone
        self.needrefresh = needrefresh
        self.time = datetime.fromisocalendar(2000, 1, 1)

        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # start chrome browser
        driver = webdriver.Chrome('TechStuff/driver.exe', options=options)

        self.browser = driver

    def run(self):
        """Запуск потока"""
        while not self.workdone.is_set():

            if not startWidgets.get_reg('WallPaper').endswith('TechStuff\\newWallpaper.jpg'):
                wh.Wallpaper.copy(copyTo='TechStuff', fileName='oldWallpaper.jpg')
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
