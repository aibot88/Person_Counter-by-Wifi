#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import re
import shlex
import datetime
import subprocess
import time

def main():
    HOST, PORT = '202.117.15.140', 8801

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST,PORT))

    while 1:
        data, addr = s.recvfrom(1024)
        data = data.decode("utf-8")
        
        if data == "Crazy seding UDP package" or not data:
            continue
        print('connect to:', addr)
        print(data)
        if data == "886":
            a = input("\n Down or Up this link ?   1 represent Up\n")
            if a is 0:
                break

if __name__ == "__main__":
    print("Center Server running successfully")
    main()
    



        