# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:13:40 2017

@author: luzhangqin
"""
#\u4E00-\u9FFF
f = open('ylk3.txt', 'r')
ylk = {}
for line in f.readlines():
    for word in line:
        if '\u4E00'<= word <= '\u9FFF':
            if word not in ylk:
                ylk[word] = 1
            else:
                ylk[word] += 1
f.close()

f = open('cp.txt', 'w')
for word in ylk:
    f.write('%s %d' %(word,ylk[word]))
    f.write('\n')
f.close()
