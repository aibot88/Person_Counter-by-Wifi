# 基于Wifi探针的定位系统

    WiFi探针是基于aircrack-ng-master的airodum-ng模块进行
    源码的编辑和修改后的程序

## 修改的功能点

    1. 将源码中的保留所有时段的WiFi信息, 改为仅显示AP附近实时探测到的MAC
    2. 将原本写入.csv文档中的信息通过UDP协议发送给服务器
    Attention: 以上功能的实现都是基于对源码的修改;
    因此ip和port需要提前修改在进行aircrack-ng的编译和安装
---

* 安装aircrack-ng的注意事项:

* 本次实验在ARM-Uuntu18.04、x86-Ubuntu14.04、x86-Kali上验证通过。
* arm-Ubuntu位于Beaglebone Black TI开发板上（BBB）
* x86-Kali位于树莓派3B上
* x86-Ubuntu位于OMEN by HP Laptop上

---

## 安装的命令

* 准备工作:
    将aircrack-ng.zip 上传到开发板上并解压缩; cd aircrack-ng目录下进行step1 --> step6
  
* step1

    ```sudo apt-get install build-essential autoconf automake libtool pkg-config libnl-3-dev libnl-genl-3-dev libssl-dev ethtool shtool rfkill zlib1g-dev libpcap-dev libsqlite3-dev libpcre3-dev libhwloc-dev libcmocka-dev hostapd wpasupplicant tcpdump screen iw usbutils```
* step2
    `sudo autoreconf -i`

* step3
    `./configure --with-experimental=true`

* step4
    ```make```
    ```ldconfig```

* step5
    ```make check```
* step6
    ```make install```
    ```make clean```

---

## 与服务器联合使用

    由于采用的是UDP传输协议。 所以server没有运行的时候， client也可以成功启动。
    想要获取client的数据只需要运行server/udpsever.py文件就可以了。
    至于server/udpdataget.py则用于求解信号源的位置。
