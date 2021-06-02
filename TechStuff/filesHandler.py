# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join

import markdown


def getItems(mypath):
    reslist = []
    onlyfiles = [f for f in sorted(listdir(mypath)) if isfile(join(mypath, f))]
    for x in onlyfiles:
        if x.endswith('.py') and not x.startswith('_'):
            try:
                print(x)
                gld = dict()
                exec(open(join(mypath, x), 'r', encoding='utf-8', errors='ignore').read(), gld, gld)
            except Exception as e:
                print(e)
                raise
                pass
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
    return reslist


if __name__ == '__main__':
    print(getItems())
