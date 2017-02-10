# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 19:29:18 2017

@author: luzhangqin
"""
import math

#前缀数组字典
def prefix(filename):
    pfarray = {}
    py = ''
    freq = 0
    totalfreq = 0
    
    f = open(filename, 'r')
    
    for line in f.readlines():
        py, freq = line.strip('\n').split(' ')[1:3:]
        totalfreq += int(freq)
        if py not in pfarray:
            pfarray[py] = int(freq)
        else:
            pfarray[py] +=  int(freq)
        wfrag =''
        for ch in py:
           wfrag += ch
           if wfrag not in pfarray:
               pfarray[wfrag] = 0
    f.close()   
    return pfarray, totalfreq

#得到又向无环图（DAG）
def getdag(pinyin, dictionary):
    DAG = {}
    tmplist = []
    ch = ''

    for id_word, word in enumerate(pinyin):
        ch = ''
        tmplist = []
        if word not in dictionary:
            pass
        else:
            for i in range(id_word, len(pinyin)):
                ch += pinyin[i]
                if ch in dictionary:
                    tmplist.append(i)
                else:
                    ch = ch[: len(ch) - 1:]
                    while not dictionary[ch]:
                       tmplist.pop()
                       ch = ch[0: len(ch) - 1:]
                       if ch == '':
                           break
                    break
        #print(tmplist)
        if not len(tmplist):
            tmplist.append(id_word)
        DAG[id_word] = tmplist
    return DAG

#动态规划 
def dp(pinyin, dictionary, DAG, totalfreq):
    route = {}
    N = len(pinyin)
    route[N] = (0, 0)
    logtotal = math.log(totalfreq)
    for idx in range(N - 1, -1, -1):
        #元组大小比较 1e-12 为了防止字典value为0的数据导致匹配成功
        route[idx] = max((math.log(
            (1e-12 if pinyin[idx:x + 1] not in dictionary.keys() else dictionary[pinyin[idx:x + 1]] or 1e-12)
                ) -logtotal + route[x + 1][0], x) for x in DAG[idx])
    return route

def translate(pinyin, route):
    begin = 0
    end = 0
    words = []
    while begin < len(pinyin):
        end = route[begin][1] + 1
        words.append(pinyin[begin:end:])
        begin = end
    return words
    
#拼音和字关联
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
    

#
def get_list(pinyin_list, dictionary):
    hz_list = []
    for word in pinyin_list:
        hz_list.append(dictionary[word])
    return hz_list

#一个字在语料库出现的次数关联
def get_cp(filename):
    f = open(filename, 'r')
    cp = {}
    for line in f.readlines():
        word, freq = line.strip('\n').split(' ')
        cp[word] = int(freq)
    f.close()
    return cp

#2元模型现在的次数关联
def get_train(filename):
    f = open(filename, 'r')
    train = {}
    for line in f.readlines():
        word, freq = line.strip('\n').split(' ')
        train[word] = int(freq)
    f.close()
    return train

#VTB算法    
def vtb(hz_list, cp, train):
    max_p = []
    first_total = 0
    total = []
    first_p = {}
    temp_p = 0
    temp_word = ''
    temp = {}
    #计算第一个列表中出现wo字的总共次数
    for line in hz_list:
        for word in line:
            first_total += 1 if word not in cp else cp[word]
        total.append(first_total)
        first_total = 0
        
    
    #计算 p=我/wo
    for word in hz_list[0]:
        temp[word] = (1 if word not in cp else cp[word]) / total[0]
    
    #VTB p=f(w1,w2)/f(w1)total
    for i in range(1, len(hz_list)):
        for j in hz_list[i]:
            for k in temp:
                if i == 1:
                    if temp_p <= (0 if k[len(k)-1] + j not in train else train[k[len(k)-1] + j]) / (1 if k[len(k)-1] not in cp else cp[k[len(k)-1]]) + temp[k]:
                        temp_p = (0 if k[len(k)-1] + j not in train else train[k[len(k)-1] + j]) / (1 if k[len(k)-1] not in cp else cp[k[len(k)-1]]) + temp[k]
                        temp_word = k + j
                else:
                    
                    if temp_p <= (0 if k[len(k)-1] + j not in train else train[k[len(k)-1] + j]) / (1 if k[len(k)-1] not in cp else cp[k[len(k)-1]]) * (0 if k[len(k)-1] not in cp else cp[k[len(k)-1]] / total[i-1]) + temp[k]:
                        temp_p = (0 if k[len(k)-1] + j not in train else train[k[len(k)-1] + j]) / (1 if k[len(k)-1] not in cp else cp[k[len(k)-1]]) * (0 if k[len(k)-1] not in cp else cp[k[len(k)-1]] / total[i-1]) + temp[k]
                        temp_word = k + j
                        
            first_p[temp_word] = temp_p
            temp_p = 0
            temp_word = ''
                
        temp = first_p
        first_p = {}
            
    max_p = sorted(temp.items(), key=lambda d:d[1], reverse = True)[0:5:]
    return max_p
        
    
if __name__ == '__main__': 
    dictionary = get_py('py.txt')
    cp = get_cp('cp.txt')
    train = get_train('train.txt')
    py_dict, totalfreq = prefix('cphz.txt')
    while True:
        pinyin = input('请输入全拼音,输入quit退出:')
        if pinyin == 'quit':
            break
        pinyin_dag = getdag(pinyin, py_dict)
        route = dp(pinyin, py_dict, pinyin_dag, totalfreq)
        pinyin_list = translate(pinyin, route)
        print(pinyin_list)
        hz_list = get_list(pinyin_list, dictionary)
        max_p = vtb(hz_list, cp, train)
        for wid, word in enumerate(max_p):
            print(str(wid + 1) + '.' + word[0] + ' ', end = '')
        print('\n')
        while True:
            idword = input('请输入id:')
            if idword in ['1','2','3','4','5']:
                break
            else:
                print('输入有误，请重新输入')
        print(max_p[int(idword)-1][0])
    
    
