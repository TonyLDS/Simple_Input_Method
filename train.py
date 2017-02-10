# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 15:13:40 2017

@author: luzhangqin
"""
#\u4E00-\u9FFF
f = open('ylk3.txt', 'r')
ylk = {}
count = 0
p = ''
for line in f.readlines():
    for word in line:
        if '\u4E00'<= word <= '\u9FFF':
            if count == 0:
                p = word
                count = 1
            else:
                if p + word not in ylk:
                    ylk[p + word] = 1
                else:
                    ylk[p + word] += 1
        else:
            count = 0
f.close()

f = open('train.txt', 'w')
for word in ylk:
    f.write('%s %d' %(word,ylk[word]))
    f.write('\n')
f.close()
