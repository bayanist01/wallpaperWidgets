# -*- coding: utf-8 -*-
import datetime
f = open("Widgets/__Время.txt", "w")
f.write(f'<h1>{datetime.datetime.now().strftime("%H:%M")}</h1>')
f.close()
