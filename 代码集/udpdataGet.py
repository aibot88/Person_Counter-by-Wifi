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


plt.close()
plt.xlim(0,15)
plt.ylim(0,10)
plt.axhline(4)
plt.axhline(6)
plt.plot([6,6],[4,0],color='b', linestyle='-')
plt.plot([10.5,10.5],[4,0],color='b', linestyle='-')
plt.plot([6,6],[10,6],color='b', linestyle='-')
plt.plot([10.5,10.5],[10,6],color='b', linestyle='-')
plt.ion()  # interactive mode on

POWER_LISR=3
list_5C = []
list_6C=[]
list_9C=[]
list_74=[]
#### 调用训练好的网络，用来进行预测
filename = r'parameters.txt'  ## 文件保存训练好的参数
net = network_0.load(filename)

r=redis.StrictRedis(host='127.0.0.1',port=6379,decode_responses=True)
sourcemacs=['5C:1D:D9:D3:04:30','9C:B2:B2:6D:06:91','74:60:FA:9C:D6:1D','6C:4D:73:3B:FC:2D']
while True:
    time.sleep(10)
    list=r.keys(pattern='train*')
    print(list)
    for key in list:
        value = r.get(key)

        if(not value):
            continue
        value_dict = json.loads(value)



        for k in value_dict:

            if (k in sourcemacs):
                power_dataframe = []
                power_list = value_dict[k]

                for i in range(0, POWER_LISR):
                    #po = 'power_list' + str(i)
                    p=power_list[i]
                    power = 0
                    if (len(p) > 0):
                        for i in range(0, len(p)):
                            power += p[i]

                        power = power / len(p)
                    power_dataframe.append(power)


                # x_train = []
                # print(power_dataframe)
                # clf=joblib.load('clf.pkl')
                # x_train.append(power_dataframe)
                # x = pd.DataFrame(x_train)
                # print(k,clf.predict(x))
                print(power_dataframe)
                x_train = np.array([[i] for i in power_dataframe])

                pre = net.feedforward(x_train)
                print(k, pre)



                rate = int(pre + 0.5)

                if (k == '5C:1D:D9:D3:04:30'):

                    if (len(list_5C) == 5):
                        print('------------------------------------------------------',list_5C)
                        rate = Counter(list_5C).most_common(1)[0][0]
                        if (rate == 3):
                            obsX = rd.uniform(1, 5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='r', marker='.')
                        if (rate == 1):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='r', marker='.')
                        if (rate == 2):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(7, 9)
                            plt.scatter(obsX, obsY, c='r', marker='.')
                        if (rate == 4):
                            obsX = rd.uniform(1, 9.5)
                            obsY = rd.uniform(5, 5)
                            plt.scatter(obsX, obsY, c='r', marker='.')
                        plt.pause(1)
                        list_5C = []
                    else:
                        list_5C.append(rate)

                if (k == '6C:4D:73:3B:FC:2D'):

                    if(len(list_6C)==5):
                        print('---------------------------------------------------', list_6C)
                        rate = Counter(list_6C).most_common(1)[0][0]
                        if (rate == 3):
                            obsX = rd.uniform(1, 5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='g', marker='^')
                        if (rate == 1):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='g', marker='^')
                        if (rate == 2):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(7, 9)
                            plt.scatter(obsX, obsY, c='g', marker='^')
                        if (rate == 4):
                            obsX = rd.uniform(1, 9.5)
                            obsY = rd.uniform(5, 5)
                            plt.scatter(obsX, obsY, c='g', marker='^')
                        plt.pause(1)
                        list_6C=[]
                    else:
                        list_6C.append(rate)

                if (k == '9C:B2:B2:6D:06:91'):

                    if(len(list_9C)==5):
                        print('---------------------------------------------------',list_9C)
                        rate = Counter(list_9C).most_common(1)[0][0]
                        if (rate == 3):
                            obsX = rd.uniform(1, 5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='b', marker='x')
                        if (rate == 1):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='b', marker='x')
                        if (rate == 2):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(7, 9)
                            plt.scatter(obsX, obsY, c='b', marker='x')
                        if (rate == 4):
                            obsX = rd.uniform(1, 9.5)
                            obsY = rd.uniform(5, 5)
                            plt.scatter(obsX, obsY, c='b', marker='x')
                        plt.pause(1)
                        list_9C=[]
                    else:
                        list_9C.append(rate)

                if (k == '74:60:FA:9C:D6:1D'):

                    if(len(list_74)==5):
                        print('---------------------------------------------------', list_74)
                        rate = Counter(list_74).most_common(1)[0][0]
                        if (rate == 3):
                            obsX = rd.uniform(1, 5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='y', marker='o')
                        if (rate == 1):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(1, 3)
                            plt.scatter(obsX, obsY, c='y', marker='o')
                        if (rate == 2):
                            obsX = rd.uniform(7, 9.5)
                            obsY = rd.uniform(7, 9)
                            plt.scatter(obsX, obsY, c='y', marker='o')
                        if (rate == 4):
                            obsX = rd.uniform(1, 9.5)
                            obsY = rd.uniform(5, 5)
                            plt.scatter(obsX, obsY, c='y', marker='o')
                        plt.pause(1)
                        list_74=[]
                    else:
                        list_74.append(rate)

