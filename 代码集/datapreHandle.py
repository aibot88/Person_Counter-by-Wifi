import re
import linecache
from pandas import read_csv
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd

def parseCsvFile(infileName,outfileNamest,outfileNameap):
    with open(infileName,'r') as f:
        lines=f.readlines()

    str_st = 'Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs'
    str_ap = 'BSSID, First time seen, Last time seen, channel, Speed, Privacy, Cipher, Authentication, Power, # beacons, # IV, LAN IP, ID-length, ESSID, Key'

    num_st=[]
    num_ap=[]

    for i in range(0,int(len(lines))):
        m=re.search(str_st,lines[i])
        n=re.search(str_ap,lines[i])
        if(m is not None):
            num_st.append(i)
        if(n is not None):
            num_ap.append(i)

    f1 = open(outfileNamest, 'w+')
    f2 = open(outfileNameap, 'w+')

    for i in num_st:
        for j in num_ap:
            if(i<j):
                start=i
                end=j
                destlines=linecache.getlines(infileName)[start:end-1]
                for key in destlines:
                    f1.write(key)
                break

    for i in num_ap:
        for j in num_st:
            if(i<j):
                start=i
                end=j
                destlines=linecache.getlines(infileName)[start:end-1]
                for key in destlines:
                    f2.write(key)
                break

    f1.close()
    f2.close()


def getLocation(filename):
    with open(filename,'r') as f:
        lines=f.readlines()
        lines1=[]
    for i in range(0,int(len(lines))):
        m=re.search("Station",lines[i])
        n=re.search(":",lines[i])
        if(m is not None):
            lines[i]=lines[i].strip("\r\n")
            lines[i]+=",location\r\n"
            tmp=lines[i].strip(',').split(',')
            lines1.append(tmp)


        if(n is not None):
            lines[i]=lines[i].strip("\r\n")
            lines[i]+=","
            lines[i]+=lines[i+1].strip("\n")
            tmp = lines[i].strip(',').split(',')
            lines1.append(tmp)


    lines2=[]
    for i in range(0,len(lines1)):

        if(len(lines1[i])!=8):
            continue
        lines2.append(lines1[i])

    return lines2

def quChong(inputFileName):
    data=getLocation(inputFileName)
    df=DataFrame(data,columns=['Station MAC', 'First time seen','Last time seen', 'Power',' packets', 'BSSID', 'Probed ESSIDs','location'])
    newDF=df.drop_duplicates()
    newDF=newDF.drop(0)
    #print(newDF)
    #print(type(newDF))

    #print(newDF.dtypes)
    #print(newDF.head())
    return newDF
def merge(df1,df2):
    df1 = df1.sort_values(by=['First time seen', 'Last time seen'], ascending=(True, True))
    df2 = df2.sort_values(by=['First time seen', 'Last time seen'], ascending=(True, True))

    df2.rename(columns={'location':'Location'},inplace=True)
    df2.rename(columns={'Power': 'power'}, inplace=True)

    listType1=df1['location'].unique()
    listType2=df2['Location'].unique()

    listType=list(set(listType1).intersection(set(listType2)))
    result=pd.DataFrame()
    tmp=pd.DataFrame()
    for i in range(0,len(listType)):

        tmp1=df1[df1['location'].isin([listType[i]])].reset_index(drop=True)
        tmp2= df2[df2['Location'].isin([listType[i]])].reset_index(drop=True)

        if(len(tmp1)==len(tmp2)):
            len1=len(tmp1)
        elif(len(tmp1)>len(tmp2)):
            len1=len(tmp1)-len(tmp2)
            drop1=tmp1.sample(n=len1, random_state=123, axis=0)

            tmp1.drop(drop1.index).reset_index(drop=True)


        else:
            len1=len(tmp2) - len(tmp1)
            tmp2.drop(tmp2.sample(n=len1,random_state=123,axis=0).index).reset_index(drop=True)
            #print('tmp2:',tmp2.sample(n=len1, random_state=123, axis=0))

        #if(not tmp1.empty and not tmp2.empty):
        tmp=pd.concat([tmp1, tmp2], axis=1, join='inner')

        #elif(not tmp1.empty):
        #    tmp=tmp1
        #elif(not tmp2.empty):
        #    tmp=tmp2
        result=result.append(tmp)
    result.drop('Location',axis=1,inplace=True)
    result=result.reset_index(drop=True)

    return result


def getData(newDF,sourcemac):
    data=newDF[newDF['Station MAC']==sourcemac]
    return data
#df=quChong()
#da=getData(df)
#print(da)
#parseCsvFile('0-test.csv','st.csv','ap.csv')
#getLocation('st.csv')
#quChong('st.csv')