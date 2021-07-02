# -*- coding: utf-8 -*-
import codecs
import os
import threading
from time import sleep

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


class Worker(threading.Thread):

    def __init__(self):
        """Инициализация потока"""
        threading.Thread.__init__(self)


    def run(self):
        """Запуск потока"""
        # получаем настройки из базы данных
        settings = db.ConfigDataBase.get('allign')[0]
        allign = 'wrap-reverse' if settings == 'right' else 'wrap'
        settings = db.ConfigDataBase.get('blockwidth')[0]
        blockwidth = int(settings)
        settings = db.ConfigDataBase.get('darktheme')[0]
        darktheme = bool(int(settings))
    # получаем файлы из которых будем делать виджеты
        items = TechStuff.filesHandler.getItems('Widgets/')
        lists = TechStuff.dirsHandler.getItems()
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

        # prepare the option for the chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # start chrome browser
        driver = webdriver.Chrome('TechStuff/chromedriver.exe', options=options)

        driver.set_window_size(*get_real_resolution())
        driver.get(os.path.abspath('TechStuff/widgets.html'))
        sleep(1)
        driver.get_screenshot_as_file("TechStuff/newWallpaper.png")
        driver.quit()

        wp.Wallpaper.set("TechStuff/newWallpaper.png")
