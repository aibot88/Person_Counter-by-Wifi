#####本程序未完成；请务必参照svm_train.py文件修改这个文件；并完成实时人数计算功能
#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import redis
import time
import json
import numpy as np
import pandas as pd
from  sklearn.externals import joblib
import my_datas_loader
import network_0
import matplotlib.pyplot as plt
import random as rd
from collections import Counter
import os


POWER_LISR=3
list_5C = []
list_6C=[]
list_9C=[]
list_74=[]
existMac={}
romCounter={}

parametersname = r'parameters.txt'  # the parameters trained before
#####################################SVM相关
net = network_0.load(parametersname)
r=redis.StrictRedis(host='127.0.0.1',port=6379,decode_responses=True)
sourcemacs=['5C:1D:D9:D3:04:30','9C:B2:B2:6D:06:91','74:60:FA:9C:D6:1D','6C:4D:73:3B:FC:2D']
while True:
    existMac={ }
    romCounter={}
    time.sleep(3)
    list=r.keys(pattern='train*')
    for key in list:
        value = r.get(key)
        
        if(not value):
            continue
        value_dict = json.loads(value)
        for k in value_dict:
            power_dataframe = []
            power_list = value_dict[k]

            for i in range(0, POWER_LISR):
                p=power_list[i]
                power = 0
                if (len(p) > 0):
                    for i in range(0, len(p)):
                        power += p[i]
                    power = power / len(p)
                power_dataframe.append(power)
            x_train = np.array([[i] for i in power_dataframe])
#################################SVM相关
            pre = net.feedforward(x_train)
            # rate = int(pre + 0.5)
            # if(len(list_74)==5):
            #     if str(rate) not in existMac:
            #         existMac[str(rate)] = []
            #         romCounter[str(rate)] = 0
            #     if k not in existMac[str(rate)]:
            #         existMac[str(rate)].append(k)
            #         romCounter[str(rate)] +=10
            #     rate = Counter(list_74).most_common(1)[0][0]
            #     list_74=[]                
            # else:
            #     list_74.append(rate)
        with open("serverdata.csv","a") as f:
            f.write('\n'+str(romCounter))