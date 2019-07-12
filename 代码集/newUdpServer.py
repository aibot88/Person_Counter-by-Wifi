#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import redis
import time
import json
import datetime
import shlex
import subprocess


table={}
dataSource={'s':[[],[],[]]}
dataMap={}

last_time=time.time()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("202.117.10.149", 8890))
print("UDP bound on port 8890...")

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
    #print(key,value)

def parseData(addr,data):
    new_table={v:k for k,v in table.items()}
    list=data.split(',')
    if(len(list)==2):
        power=int(list[1])
        if(power==-1):
            return
        yuanzu=int(list[1])
        index=new_table[addr[0]]
        if(not (list[0] in dataSource.keys())):
            dataSource[list[0]]=[[],[],[]]
            dataMap[list[0]]=[]
        dataSource[list[0]][index].append(yuanzu)
        dataMap[list[0]].append(index)

def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        参数:
    cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
    timeout: 超时时间，秒，支持小数，精度0.1秒
    shell: 是否通过shell运行
    Returns: return_code
    Raises: Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, bufsize=4096)            
    time.sleep(0.1)
    if timeout:
        if end_time <= datetime.datetime.now():
            raise Exception("Timeout：%s"%cmdstring)
        return str(sub.returncode)

def main():
    execute_command('python3 udpdataGet.py')
    while True:
        data, addr = s.recvfrom(1024)
        data = str(data, encoding="utf8")
        print("Receive from %s:%s" % addr, data)
        if data == b"exit":
            s.sendto(b"Good bye!\n", addr)
        if data.startswith('table'):
            table[int(data[5])] = addr[0]
            continue
        parseData(addr, data)
        global last_time
        while((time.time()-last_time)>10):
            timedPreservation()
            last_time=time.time()


if __name__==('__main__'):
    print('ts successs')
    main()