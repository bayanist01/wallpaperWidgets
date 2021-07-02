# -*- coding: utf-8 -*-
import sqlite3
import threading



class ConfigDataBase:
    lock = None
    # Создание таблицы
    @classmethod
    def createtable(cls):
        cls.lock = threading.Lock()
        with cls.lock:
            cls.conn = sqlite3.connect("TechStuff/config.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
            cls.cursor = cls.conn.cursor()
            cls.cursor.execute("""CREATE TABLE IF NOT EXISTS config
                                  (name text UNIQUE, param text)
                               """)
            cls.conn.commit()

    @classmethod
    def getall(cls):
        with cls.lock:
            cls.conn = sqlite3.connect("TechStuff/config.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
            cls.cursor = cls.conn.cursor()
            cls.cursor.execute('SELECT * FROM config')
            reslist = cls.cursor.fetchall()
            cls.conn.commit()
        return reslist

    @classmethod
    def set(cls, name, param):
        with cls.lock:
            cls.conn = sqlite3.connect("TechStuff/config.db",
                                       check_same_thread=False)  # или :memory: чтобы сохранить в RAM
            cls.cursor = cls.conn.cursor()
            cls.cursor.execute('REPLACE INTO config (name, param) VALUES(?, ?)', (name, param))
            reslist = cls.cursor.fetchall()
            cls.conn.commit()
        return reslist

    @classmethod
    def get(cls, name):
        with cls.lock:
            cls.conn = sqlite3.connect("TechStuff/config.db",
                                       check_same_thread=False)  # или :memory: чтобы сохранить в RAM
            cls.cursor = cls.conn.cursor()
            cls.cursor.execute('SELECT param FROM config WHERE name = ?', (name,))
            reslist = cls.cursor.fetchone()
            cls.conn.commit()
        return reslist

    @classmethod
    def closetable(cls):
        with cls.lock:
            cls.cursor.close()
            cls.conn.commit()
            cls.conn.close()
