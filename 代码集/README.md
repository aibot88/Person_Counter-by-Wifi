# Server程序的更新和安卓发包程序UDPdemo的开发

对雷丹学姐的server和process程序进行了微调; 并开发了一款安卓udp发包程序并成功在市场上找到一款苹果发包程序

## Server程序的微调

### 功能的变化

对server和dataget进行的功能性调整

- 启动server.py程序后自动运行dataget.py
- dataget.py程序的实现自动总结各个房间的人数(目前只有2号房间的人数,因为只有二号的板子,所以预测结果全是2号房间);暂且存入一个csv文件,日后会直接发送给服务器

### 运行环境

- Ubuntu 18.04LTS的python3.7环境下; 使用pip3安装所有的依赖包后直接运行python3 newUdpServer.py
- PersionLoaction文件夹中的相关依赖文件都是必要的

### 修改说明

对server和dataget程序修改的详细说明

#### server

- 删除一些无用的调试print
- 增加`def execute_command(cmdstring, cwd=None, timeout=None, shell=False):`子进程函数用于同时运行dataget

#### dataget

- 删除所有的作图程序
- 出于实验环境的考虑,目前的统计人数是基于mac地址的而不是基于手机mac的;因此手机mac需要重新筛选
- `existMac[str(rate)] = []`和`romCounter[str(rate)] = 0`是用于人数统计的变量.想要定位人数统计程序部分只需要ctrl+f 搜索此变量所在位置即可

### 特别注意

所有的ip地址和端口号都是在程序里面写死的,因此需要提前核对;目前所有的板子的发送ip都是202.117.10.149

## 发包程序

介绍两款发包程序的使用方法;主要是安卓版的.

### 发包程序的简介

苹果版发包程序可在Appstore下载安装,搜索UDP即可; 安卓版的发包程序见上级目录下UDPSocketDemo-master文件夹;直接用Android studio即可打包到任一安卓手机使用;目前安装在红米1s上.

### 发包程序使用说明

苹果发包程序可以自定义udp的地址端口和信息等,不需要说明; 
由于时间有限,因此安卓版的将ip和port写死在了程序里面ip是202.117.15.140; port=8801. 

可在UDPSocketDemo-master\app\src\main\java\melo\com\udpsocketdemo\socket下的`UDPSocket.java`进行修改. 如果时间允许的话我尽量将安卓程序做的和苹果程序一样.

### 注意

- 安卓程序的点击一次持续发包1分钟(每秒100个UDP包), 在此期间程序会卡住不能动;这是正常现象.一分钟之后再次点击send又会进行新一轮疯狂发包.
发包调试server.py打印出来的是你发送的有效包的内容;这个包每秒发送1个;用来标记你的实际坐标. 而苹果程序点一次只能发一个包.
- 目前的调试server.py的信息还不知道怎么和学姐你的udpserver.py的数据进行共享;没有办法直接将坐标信息和airodump抓包的信息融合起来;直接给出`[mac, location, signal, signal, signal]`的元组
