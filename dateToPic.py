#coding:utf-8
import os
import re
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
#from xlwt import *

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fftpack import fft, ifft
from scipy import signal
#from tqdm import tnrange, tqdm_notebook

import matplotlib as mpl
mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号

path = '../../试验数据'
pathPic = '../../试验数据pic'
#path_time = 'E:/试验数据time/time.txt'
path_time = './time.txt'
hz = 12800
#myfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/SimHei.ttf')
myfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/win10/Fonts/msyh.ttc')
mpl.rcParams['axes.unicode_minus'] = False
cl = ['k','red','blue','lime','dodgerblue','m']
# plt.rc('font', family='SimHei', size=8) #Chinese font    

def read_csv(path):
    f = pd.read_csv(path,sep = '\t',skiprows = 4,header = None,engine = 'python')
    f.columns = ['x','y','z']
    return f

def picDrawGrp(x,y,labels,zongji,path,picName,log=True,hz=12800):
    #picName = path[-9:-4]
    fig = plt.figure(figsize=(10,5),dpi=200)
    axes = fig.add_axes([0.1,0.1,0.8,0.8])
    # plt.text(40,115,'10Hz-200Hz总级(dB)',fontsize=10,\
    #         verticalalignment='center',horizontalalignment='center',fontproperties=myfont)
    for index in range(len(x)):
        axes.plot(x[index][::2], y[index][::2],linewidth = 0.5,color = cl[index],label = labels[index] + ' 25Hz-30Hz总级:' + str(round(zongji[index],2)))
        #axes.plot(x[index][::2], y[index][::2],linewidth = 0.5,color = cl[index],label = labels[index])
        # plt.text(40,115- (index+1) * 7,labels[index] + ': ' + str(round(zongji[index],2)),fontsize=10,\
        #     verticalalignment='center',horizontalalignment='center',fontproperties=myfont)
    
        if log == True:
            axes.set_ylim(0,120)
            axes.set_ylabel('dB',fontproperties=myfont,fontweight='black')
        else:
            y_max = []
            tmp = [xtmp - 10 for xtmp in x[index]]
            x_abs1 = [np.abs(i) for i in tmp]
            x_arg1 = np.argmin(x_abs1)

            tmp = [xtmp - 200 for xtmp in x[index]]
            x_abs2 = [np.abs(i) for i in tmp]
            x_arg2 = np.argmin(x_abs2)
            y_max.append(np.max(y[index][x_arg1:x_arg2]))
            
            axes.set_ylim(0,1.2 * np.max(y_max))
            axes.set_yticks(np.arange(0,round(1.2 * np.max(y_max),2)),10)
            #axes.set_ylim(0,0.02)
            if re.search('压力',labels[index]):
                axes.set_ylabel('kPa',fontproperties=myfont,fontweight='black')
            else:
                axes.set_ylabel('g',fontproperties=myfont,fontweight='black')
    plt.legend(loc='upper right')
    #axes.scatter(npfr[signal.argrelextrema(npxfp,np.greater)[0]],npxfp[signal.argrelextrema(npxfp, np.greater)[0]],s=10,c='r',marker='o')
    #axes.annotate(npfr[signal.argrelextrema(npxfp,np.greater)[0]],npxfp[signal.argrelextrema(npxfp, np.greater)[0]])
    #axes.scatter(freqs, xfp,linewidth = 0.3,color = 'k')
    axes.set_xlim(10,200)
    axes.set_xticks(np.linspace(10,200,20,endpoint=True))
    #plt.text(200,-1.5,'200',fontsize=10,\
    #        verticalalignment='top',horizontalalignment='center')
    #axes.set_ylim(0,np.max(npxfp[int(10.0*len(x)/20000.0):])*1.2)
    #print('np.max(npxfp)*1.2    ' + str(np.max(npxfp)*1.2))
    axes.set_xlabel(u'频率/Hz',fontproperties=myfont,fontweight='black')
    
    axes.set_title(picName,fontproperties=myfont,fontweight='black')
    axes.grid(color='black', alpha=0.5, linestyle='dashed', linewidth=0.5)
    #plt.show()
    fig.savefig(path)
    plt.close()

# def smooth(data,num=11):
#     res = []
#     for i in range(0,len(data)):
#         if i <= len(data)-int(num/2)-1 and i >=int(num/2):
#             if type(data[i-int(num/2):i+int(num/2)]) == type([]):
#                 lvbo = data[i-int(num/2):i+int(num/2)]
#             else:
#                 lvbo = data[i-int(num/2):i+int(num/2)].tolist()
#             res.append(max(lvbo,key=lvbo.count))
#         else:
#             res.append(data[i])
#     return res

def smooth(data,num=11):
    return data

def FFT(dataArrayXX,dataArrayYY,hz ,log=True):
    x = np.array(dataArrayXX)
    y = np.array(dataArrayYY)
    sampling_rate = hz
    #print(len(x))
    #print(sampling_rate)
    #yy=fft(y)                     #快速傅里叶变换
    #yreal = yy.real               # 获取实数部分
    #yimag = yy.imag               # 获取虚数部分
    #print(yreal)
    yf=abs(fft(y))                # 取绝对值
    yf1 = yf/len(x)*2     #归一化处理
    yf2 = yf1[range(int(len(x)/2))]#由于对称性，只取一半区间

    xf1 = np.linspace(0,sampling_rate,len(x))
    xf2 = xf1[range(int(len(xf1)/2))]
    #npfr = np.array(xf2)
    #get log10
    zongji = 0
    print(xf2)
    dx = xf2[5] -xf2[4]
    #print('dx: ',dx)
    #print(yf2)
    for index,i in enumerate(xf2):
        if i >= 25 and i <= 30:
            zongji += dx * (yf2[index] ** 2)
    zongji = 20 * np.log10(np.sqrt(zongji) / 1e-6)
    if log == True:
        npxfp = 20*np.log10(np.clip(yf2,1e-20,1e100)/1e-6)
    else:
        npxfp = yf2
    #npxfp = np.array(yf2)
    # fig = plt.figure(figsize=(8,4),dpi=200)
    # axes = fig.add_axes([0.1,0.1,0.8,0.8])
    # axes.plot(xf2, npxfp,linewidth = 0.3,color = 'k')
    return [xf2,npxfp,zongji]

def get_time_available(path_time):
    dic_time = {}
    with open(path_time,encoding='gbk') as f:
        for i in f.readlines(): #实船格栅5节阀门全关 39-41s
            time_list = i.split(' ')
            #print(time_list)
            dic_time[time_list[0]] = [int(time_list[1].strip()[0:2]),int(time_list[1].strip()[-3:-1])]
    return dic_time

def get_file_name(path):
    result = []
    for root,_,files in os.walk(path):
        for file in files:
            result.append(root + os.sep + file)
    return result


def plot_by_re(reStr,log=True,lvbo = 0,file_path='./udf.png',pic_title=''):
    cedian_act = ['加速度测点1','加速度测点2','加速度测点3','加速度测点4','加速度测点5','加速度测点6','加速度测点7','加速度测点8', \
                '压力测点1','压力测点2','压力测点3','压力测点4','压力测点5','压力测点6','压力测点7','压力测点8']
    dic_time = get_time_available(path_time)
    file_name = get_file_name(path)
    file_group = []
    label = []
    zongji = []
    pic_re = ''
    point = []
    hz = 12800
    for file in file_name:
        #print(xx)
        flag = 1
        tmp_point = ''        
        for index,ii in enumerate(reStr):
            pic_re += ii
            if index == 0:
                flag = 1
                #print(index)
            if re.search(re.compile(r'测点'),ii):
               
                ii_t = '\(' + ii[2:] + '\).txt' #\(6\).txt
                tmp_point = ii
                #print(ii_t)
            else:
                ii_t = ii
            if re.search(re.compile(ii_t),file):
                #print(ii_t,'pass')
                pass
            else:
                flag = 0
            if index == len(reStr) -1 and flag == 1:
                file_group.append(file)
                point.append(tmp_point)
                print(file,'pass')
                #print(tmp_point)
        
    date_group_x = []
    date_group_y = []
    # print(file_group)
    for index,i in enumerate(file_group):
        print(i.split('/')[-2])
        if i.split('/')[-2] == '优化格栅一号1节阀门全开' or \
            i.split('/')[-2] == '优化格栅一号2节阀门全开' or \
            i.split('/')[-2] == '优化格栅一号3节阀门全开' or \
            i.split('/')[-2] == '优化格栅一号4节阀门全开' or \
            i.split('/')[-2] == '优化格栅一号5节阀门全开' or \
            i.split('/')[-2] == '优化格栅一号6节阀门全开':
                hz = 1280
                print('hz :' + str(hz))
        else:
            hz = 12800
            print('hz :' + str(hz))
        print(i + ' is reading... ')
        datafm = read_csv(i)
        x = datafm['x']
        y = datafm['y']
        #print(y)
        start_point = dic_time[i.split('/')[-2]][0] * hz
        end_point = dic_time[i.split('/')[-2]][1] * hz
        print(start_point,'   ',end_point)
        # x = np.array(x[start_point:end_point])
        # y = np.array(y[start_point:end_point])
        if re.search(r'实船',i.split('/')[-2]):
            #x = np.array(x[start_point:end_point])
            #y = np.array(y[start_point:end_point])
            x = np.array(x[end_point - 5 * hz:end_point])
            y = np.array(y[end_point - 5 * hz:end_point])
        else:
            start_point = end_point - 5 * hz
            x = np.array(x[end_point - 5 * hz:end_point])
            y = np.array(y[end_point - 5 * hz:end_point])
        #print('smoothing...')
        y = smooth(y)
        if lvbo != 0:
            print('lvbo .....')
            b,a = signal.butter(3,2 * lvbo / hz,'low')
            sf = signal.filtfilt(b,a,y)
            y = sf
            
        #print(y)
        print('calculating FFT...')
        fftx,ffty,zongji_single = FFT(x,y,hz=hz,log=log)
        zongji_check(i.split('/')[-2] + point[index],zongji_single,start_point,end_point,reStr,log=log,lvbo = lvbo,file_path=file_path,pic_title=pic_title,hz=hz)
        zongji.append(zongji_single)
        date_group_x.append(fftx)
        date_group_y.append(ffty)
        
        label.append(i.split('/')[-2] + cedian_act[int(''.join(point[index][2:])) - 1])
    print('Drawing picGroup...',len(date_group_x))
    picDrawGrp(date_group_x,date_group_y,label,zongji,file_path,picName = pic_title,log=log)
    print('finished')

def zongji_check(file_name,zongji,start_point,end_point,reStr,log=True,lvbo = 0,file_path='./udf.png',pic_title='',hz=12800):
    time_zongji = open('time_and_zongji.txt','a+')
    time_zongji.write(file_name + ',' + str(zongji) + '\n')
    # lines = []
    # if file_name[0:2] != '实船':
    #     lines = time_zongji.readlines()
    #     for _id,line in enumerate(lines):
    #         if line.split(',')[0] == r'实船' + file_name[-6:] and float(line.split[1]) < zongji - 0.3:
    #             lines[_id] = file_name + ',' + str(zongji - hz) + ',' + str(start_point -hz) + ',' + str(end_point) + 'changed\n'
    #             print(file_name + 'reploting...')
    #             with open('time_and_zongji.txt','w') as f:
    #                 f.writelines(lines)
    #             return plot_by_re(reStr,log=log,lvbo = lvbo,file_path=file_path,pic_title=pic_title)
    
    return True


    pass
