# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 23:29:22 2017

@author: luzhangqin
"""

def get_py(filename):
    hz = ''
    py = ''
    zm = ''
    
    dictionary = {}
    
    f = open(filename, 'r')
    for line in f.readlines():
        hz, py, zm = line.strip('\n').split(',')
        if py not in dictionary:
            dictionary[py] = [hz]
        else:
            dictionary[py].append(hz)
    f.close()
    return dictionary


if __name__ == '__main__': 
    dictionary = get_py('py.txt')