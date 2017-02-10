# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:18:12 2017

@author: luzhangqin
"""
ylk  = []
hzcp = []
ylk2 = []
hzcppy = []

f1 = open('cp.txt' ,'r')
for line in f1.readlines():
    hz, cp = line.strip('\n').split(' ')
    hzcp.append(hz)
    hzcp.append(cp)
    ylk.append(hzcp)
    hzcp = []
f1.close

f2 = open('py.txt', 'r')
for line in f2.readlines():
    hz, py, = line.strip('\n').split(',')[:2:]
    hzcppy.append(hz)
    hzcppy.append(py)
    ylk2.append(hzcppy)
    hzcppy = []
f2.close()    

f3 = open('cphz.txt', 'w')
flag = 0
for word in ylk2:
    for word1 in ylk:
        if word[0] == word1[0]:
            flag = word1[1]
    
    f3.write('%s %s %s\n' %(word[0], word[1], flag))

    flag = 0    
f3.close()        