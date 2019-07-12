#!/usr/bin/env python3.7
#code by "utf-8"
from sys import argv,exit
from svm import *
from svmutil import *


def help():
    print("\nWe will show you this message when is programme is exit(error), please read it carefully. If you want to read again, Please using -h \n ")
    print("-c train or test; to tell the programme weather you want to train or test\n")
    print("-f filename.csv[or otherFilename.type]; to assign the data you want to train or predict\n")
    print("-m filename[or other paramentname.type]; to assign the model you want to use for prediction\n")

def train(filepath = "基于信号强度的定位/代码集/udptraindata.csv", parameter = '-c 4'):
    y,x = svm_read_problem(filepath)
    prob = svm_problem(y,x)
    param = svm_parameter(parameter)
    model = svm_train(prob, param)
    svm_save_model('基于信号强度的定位/代码集/model',model)

#如果你想使用预测函数来检验你的模型的正确率；只需要将accuracy变量print就可以了
def predict(filepath = "基于信号强度的定位/代码集/test.csv", modelname = 'model'):
    y , x = svm_read_problem(filepath)
    model = svm_load_model(modelname)
    l, accuracy, vals = svm_predict(y, x, model)
    print(l)
    print(accuracy)

def main():
    flag = 10
    filepath = "基于信号强度的定位/代码集/udptraindata.csv"
    modelname = '基于信号强度的定位/代码集/model'
    length = len(argv)
    if length > 1:
        for index,item in enumerate(argv):
            # print(index,item)
            if item == "-h":
                help()
            if item == "-c":
                if argv[index+1] == "train":
                    flag = 1
                elif argv[index+1] == "test":
                    flag = 0
            if item == "-f":
                filepath = argv[index + 1] 
            if item == "-m":
                modelname = argv[index + 1]
    if flag == 1:
        print("Running svm_train successfully, the Model_file will be stored in your running path.")
        param = '-c 4'
        train(filepath,param)
    elif flag == 0:
        print("Running svm_predict successfully, we use the model.model file in your runing path as predict_condition.")
        predict(filepath, modelname)
    
if __name__ == "__main__":
    exit(main())