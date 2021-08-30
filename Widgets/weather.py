# -*- coding: utf-8 -*-
import requests
import os

r = None

try:
    r = requests.get('https://wttr.in/?0TQ&lang=ru')
except Exception:
    pass

if r:
    f = open("Widgets/__Погода.txt", "w", encoding='utf-8')
    f.write(f'<pre style="font-size: 17px">{r.text}</pre>')
    f.close()
else:
    if os.path.exists("Widgets/__Погода.txt"):
        os.remove("Widgets/__Погода.txt")

