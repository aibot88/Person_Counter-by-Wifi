# 基于信号强度的person_Counter

## 目录

基于强度的personCounter ----- 工具包 ------ libsvm
                        |            |
                        |            --- aircrack-ng-master.zip
                        |            |
                        |            --- UDPsenderDemoMaster
                        |            |
                        |            --- README.md
                        |
                        --- 数据集 ------ udptraindata.csv
                        |            |
                        |            --- model
                        |            |
                        |            --- test.csv
                        |            |
                        |            --- test_result.csv
                        |
                        --- 代码集 ------ udpserver1.py
                                     |
                                     --- udpdataget.py
                                     |
                                    --- udpserverCsv.py
                                    |
                                    --- udpdataGettoCsv.py
                                    |
                                    --- svm_train_predict.py
                                    |
                                    --- README.md
## 必要的说明

### 工具包
`airacrack-ng-master` 的使用参阅工具包目录的README.md
`UdpsenderDemomaster` 需要使用Android Studio打开完整的project，想要修改的话参阅代码集的Readme
`libsvm` 的使用参阅libsvm/python目录下的README.md

### 数据包

放置了训练数据，保存的参数，预测数据，预测结果

### 代码集

放置了必要的处理机代码，`server`的数据接收程序和`svm_tran_predict`训练处理程序