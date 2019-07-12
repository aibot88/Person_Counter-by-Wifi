import matplotlib.pyplot as plt
import numpy as np
import math
import random as rd
import csv

filename = 'udptraindata.csv'
data = []
with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        if (row[0] == '5C:1D:D9:D3:04:30' or row[0] == '6C:4D:73:3B:FC:2D' or row[0] == '9C:30:5B:B8:AE:6F' or row[
            0] == '74:60:FA:9C:D6:1D'):
            dr = [row[1], row[2], row[3], row[4], row[0]]
            data.append(dr)

plt.close()
plt.xlim(0, 15)
plt.ylim(0, 10)
plt.axhline(4)
plt.axhline(6)
plt.plot([6, 6], [4, 0], color='b', linestyle='-')
plt.plot([10.5, 10.5], [4, 0], color='b', linestyle='-')
plt.plot([6, 6], [10, 6], color='b', linestyle='-')
plt.plot([10.5, 10.5], [10, 6], color='b', linestyle='-')
plt.ion()  # interactive mode on
for i in range(len(data)):
    xs = [float(data[i][0]), float(data[i][1]), float(data[i][2])]
    name = data[i][4]
    if (name == '5C:1D:D9:D3:04:30'):
        rate = int(data[i][3])
        if (rate == 3):
            obsX = rd.uniform(0, 6)
            obsY = rd.uniform(0, 4)
            plt.scatter(obsX, obsY, c='r', marker='.')
        if (rate == 1):
            obsX = rd.uniform(6, 10.5)
            obsY = rd.uniform(0, 4)
            plt.scatter(obsX, obsY, c='r', marker='.')
        if (rate == 2):
            obsX = rd.uniform(6, 10.5)
            obsY = rd.uniform(6, 10)
            plt.scatter(obsX, obsY, c='r', marker='.')
        if (rate == 4):
            obsX = rd.uniform(0, 10.5)
            obsY = rd.uniform(4, 6)
            plt.scatter(obsX, obsY, c='r', marker='.')

    if (name == '6C:4D:73:3B:FC:2D'):
        rate = int(data[i][3])
        if (rate == 3):
            obsX = rd.uniform(0, 6)
            obsY = rd.uniform(0, 4)
            plt.scatter(obsX, obsY, c='g', marker='x')
        if (rate == 1):
            obsX = rd.uniform(6, 10.5)
            obsY = rd.uniform(0, 4)
            plt.scatter(obsX, obsY, c='g', marker='x')
        if (rate == 2):
            obsX = rd.uniform(6, 10.5)
            obsY = rd.uniform(6, 10)
