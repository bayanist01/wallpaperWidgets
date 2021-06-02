# -*- coding: utf-8 -*-
import requests
f = open("Widgets/_Погода.txt", "w", encoding='utf-8')
r = requests.get('https://wttr.in/?0TQ&lang=ru')

f.write(f'<pre style="font-size: 17px">{r.text}</pre>')
f.close()
