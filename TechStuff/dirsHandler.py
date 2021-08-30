# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join

import TechStuff.filesHandler


def get_items():
    reslist = []
    mypath = 'Widgets/'
    onlydirs = [f for f in sorted(listdir(mypath)) if not isfile(join(mypath, f))]
    for x in onlydirs:
        if x.startswith('_'):
            continue
        item = {'name': x, 'content': TechStuff.filesHandler.get_items(join(mypath, x))}
        reslist.append(item)
    return reslist
