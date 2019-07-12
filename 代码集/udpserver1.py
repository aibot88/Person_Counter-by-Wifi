#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import redis
import time
import json

table={}
dataSource={'s':[[],[],[]]}
dataMap={}

print(dataSource)
last_time=time.time()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("202.117.15.142", 8890))
print("TCP bound on port 8890...")


def timedPreservation():

    r=redis.StrictRedis(host='127.0.0.1',port=6379,decode_responses=True)
    global dataSource
    global dataMap
    value= json.dumps(dataSource)
    dataSource={}
    dataMap={}
    key=time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime())
    key='train'+key
    r.set(key, value)
    r.expire(key,100)
    print(key,value)

def parseData(addr,data):
    new_table={v:k for k,v in table.items()}
    list=data.split(',')

    if(len(list)==2):
        power=int(list[1])
        if(power==-1):
            return

        yuanzu=int(list[1])
        index=new_table[addr[0]]
        print(index)
        if(not (list[0] in dataSource.keys())):
            dataSource[list[0]]=[[],[],[]]
            dataMap[list[0]]=[]

        dataSource[list[0]][index].append(yuanzu)
        dataMap[list[0]].append(index)

        print(dataSource)
        print(dataMap)


    else:
        for i in range(0,len(list)):
            print(list[i].strip())

def main():

    while True:
        try:
            clientSocket, clientAddr = s.accept()
        except:
            pass
        else: 
            data, addr = clientSocket.recvfrom(1024)
            data = str(data, encoding="utf8")

            print("Receive from %s:%s" % addr, data)

            if data == b"exit":
                s.sendto(b"Good bye!\n", addr)
            if data.startswith('table'):
                table[int(data[5])] = addr[0]
                print(table)
                continue

            parseData(addr, data)
            global last_time
            print(time.time()-last_time)
            while((time.time()-last_time)>10):
                timedPreservation()
                last_time=time.time()


if __name__==('__main__'):


    print('ts successs')
    main()


