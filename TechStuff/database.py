# -*- coding: utf-8 -*-
import contextlib
import sqlite3
import threading


class ConfigDataBase:
    lock = threading.Lock()

    # Создание таблицы
    @classmethod
    def createtable(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect("TechStuff/config.db", check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute("""CREATE TABLE IF NOT EXISTS config
                                          (name text UNIQUE, param text) """)

    @classmethod
    def getall(cls):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect("TechStuff/config.db", check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT * FROM config')
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def set(cls, name, param):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect("TechStuff/config.db", check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('REPLACE INTO config (name, param) VALUES(?, ?)', (name, param))
                    reslist = cursor.fetchall()
        return reslist

    @classmethod
    def get(cls, name):
        with cls.lock:
            with contextlib.closing(
                    sqlite3.connect("TechStuff/config.db", check_same_thread=False, isolation_level=None)) as conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute('SELECT param FROM config WHERE name = ?', (name,))
                    reslist = cursor.fetchone()
        return reslist

