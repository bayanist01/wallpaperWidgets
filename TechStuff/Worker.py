# -*- coding: utf-8 -*-
import codecs
import os
import threading
import datetime

import win32gui
import win32print
from jinja2 import Environment, FileSystemLoader, select_autoescape
from selenium import webdriver
from win32.lib import win32con

import TechStuff.database as db
import TechStuff.dirsHandler
import TechStuff.filesHandler
import TechStuff.wallpaperHandler as wp


def get_real_resolution():
    """Get the real resolution"""
    hDC = win32gui.GetDC(0)
    # Horizontal resolution
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # Vertical resolution
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def createBrowser():
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # start chrome browser
    driver = webdriver.Chrome('TechStuff/driver.exe', options=options)
    return driver


class Worker(threading.Thread):

    def __init__(self, browser=None):
        threading.Thread.__init__(self)
        self.browser = browser if browser is not None else createBrowser()

    def run(self):
        start = datetime.datetime.now()

        # получаем настройки из базы данных
        settings = db.ConfigDataBase.getall()
        settings = {name: content for name, content in settings}

        allign = 'wrap-reverse' if settings['allign'] == 'right' else 'wrap'
        blockwidth = int(settings['blockwidth'])
        darktheme = bool(int(settings['darktheme']))

        settings = datetime.datetime.now()
        print(f'Settings: {settings - start}')

        # получаем файлы из которых будем делать виджеты
        items = TechStuff.filesHandler.getItems('Widgets/')
        lists = TechStuff.dirsHandler.getItems()

        getitems = datetime.datetime.now()
        print(f'GetItems:{getitems - settings}')

        # подключаем шаблон html- страницы
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('TechStuff/template.html')
        rendered_page = template.render(
            path_to_old_wallpaper='oldWallpaper.jpg',
            row_column='column',
            is_reverse=allign,
            bg_rgb_color='0,0,0' if darktheme else '255,255,255',
            bg_opacity='0.7',
            text_rgb_color='200,200,200' if darktheme else '0,0,0',
            width_percent=blockwidth,
            blocks=items,
            lists=lists
        )

        with codecs.open("TechStuff/widgets.html", "w", "utf-8") as temp:
            temp.write(rendered_page)

        templatetime = datetime.datetime.now()
        print(f'TemplateWorks: {templatetime - getitems}')

        driver = self.browser
        driver.set_window_size(*get_real_resolution())
        drivertimestart = datetime.datetime.now()
        driver.get(os.path.abspath('TechStuff/widgets.html'))
        driver.get_screenshot_as_file("TechStuff/newWallpaper.png")
        drivertimestop = datetime.datetime.now()
        print(f'driverWorks: {drivertimestop - drivertimestart}')

        screenshot = datetime.datetime.now()
        print(f'Screenshot: {screenshot - getitems}')

        wp.Wallpaper.set("TechStuff/newWallpaper.png")

        stop = datetime.datetime.now()
        print(f'WpSet: {stop - screenshot}')

        delta = stop - start
        print(delta)
