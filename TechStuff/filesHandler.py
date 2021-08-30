# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join

import markdown
from datetime import datetime


def getItems(mypath):
    start = datetime.now()
    reslist = []
    onlyfiles = [f for f in sorted(listdir(mypath)) if isfile(join(mypath, f))]
    startpy = datetime.now()
    for x in onlyfiles:
        if x.endswith('.py') and not x.startswith('_'):
            try:
                # TODO сделать быстее
                gld = dict()
                exec(open(join(mypath, x), 'r', encoding='utf-8', errors='ignore').read(), gld, gld)
            except Exception as e:
                print(e)

    stoppy = datetime.now()
    print('EXEC', stoppy-startpy)

    for x in onlyfiles:
        if x.endswith('.txt'):
            with open(join(mypath, x), encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            item = {'name': x[:-4].lstrip('_'), 'content': ''.join(lines).replace('\n', '<br>')}
            reslist.append(item)
        if x.endswith('.md'):
            with open(join(mypath, x), encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            content = ''.join(lines)
            item = {'name': x[:-3].lstrip('_'),
                    'content': markdown.markdown(content)}
            reslist.append(item)

    stop = datetime.now()
    print('ALL', stop-start)

    return reslist
