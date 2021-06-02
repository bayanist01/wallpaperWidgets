# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join

import TechStuff.filesHandler


def getItems():
    reslist = []
    mypath = 'Widgets/'
    onlydirs = [f for f in sorted(listdir(mypath)) if not isfile(join(mypath, f))]
    for x in onlydirs:
        if x.startswith('_'):
            continue
        item = {'name': x, 'content': TechStuff.filesHandler.getItems(join(mypath, x))}
        reslist.append(item)
    return reslist


if __name__ == '__main__':
    print(getItems())
