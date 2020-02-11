import config
import numpy as np
from scipy.signal import argrelmax,argrelmin
import matplotlib.pyplot as plt
from statistics import mean
import statistics

def mute_ramp (data):
    list_to_analyze=[]
    data_1=[]
    data_2=[]
    for i,j in enumerate(data):
        list_to_analyze.extend(data[i][0])
        if i<=4 :
            data_1.append(data[i][1])
        if i>= len(data)-5:
            data_2.append(data[i][1])
    mediana=[np.median(data_1),np.median(data_2)]
    if mediana[0]==0 and mediana[1]==0:
        __data_to_analyze__ = []
        list_to_analyze = [list_to_analyze[i * 100:(i + 1) * 100] for i in range(int(len(list_to_analyze) / 100))]
        for i in list_to_analyze:
            __data_to_analyze__.append(np.amax(i))
        ret = (("{}, {}".format(fallingramp(__data_to_analyze__),raisingramp(__data_to_analyze__))))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))

        # config.__mute_ramp_result__.insert(0,"{}, {}".format(fallingramp(__data_to_analyze__),raisingramp(__data_to_analyze__)))
        try:
            config.__mute_ramp_result__.pop(1)
        except IndexError:
            return-1
        return (("{}, {}".format(fallingramp(__data_to_analyze__), raisingramp(__data_to_analyze__))))
    elif mediana[0]==0 and mediana[1]==-1:
        __data_to_analyze__ = []
        list_to_analyze = [list_to_analyze[i * 100:(i + 1) * 100] for i in range(int(len(list_to_analyze) / 100))]
        for i in list_to_analyze:
            __data_to_analyze__.append(np.amax(i))
        ret = (fallingramp(__data_to_analyze__))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))
        # config.__mute_ramp_result__.insert(0,fallingramp(__data_to_analyze__))
        try:
            config.__mute_ramp_result__.pop(1)
        except IndexError:
            return -1
        return (fallingramp(__data_to_analyze__))
    elif mediana[0]==-1 and mediana[1]==0:
        __data_to_analyze__ = []
        list_to_analyze = [list_to_analyze[i * 100:(i + 1) * 100] for i in range(int(len(list_to_analyze) / 100))]
        for i in list_to_analyze:
            __data_to_analyze__.append(np.amax(i))
        ret = (raisingramp(__data_to_analyze__))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))
        # config.__mute_ramp_result__.insert(0,raisingramp(__data_to_analyze__))
        try:
            config.__mute_ramp_result__.pop(1)
        except IndexError:
            return -1
        return (raisingramp(__data_to_analyze__))
    if mediana[0] == -1 and mediana[1] == -1:
        return -1
    return-1

def fallingramp(data):
    counter = 0
    maksimumms=list()
    # plt.subplots(2,1)
    # plt.subplot(2,1,1)
    # plt.plot(data)
    data = [data[i * 10:(i + 1) * 10] for i in range(int(len(data) / 10))]
    for k,j in enumerate(data):
        ret=np.average(np.gradient(j))
        if ret <-0.5:
            maksimumms.extend(j)
    max = np.amax(maksimumms[:50])
    ret=np.argmax(maksimumms[:50])
    for i,j in enumerate(maksimumms):
        if i >ret and j<max*0.97:
            counter+=1
            if j<50:
                break
    # print("counter", counter)
    # plt.subplot(2,1,2)
    # plt.plot(maksimumms)
    # plt.title('failing ramp')
    # plt.show()
    return ("Falling ramp: {} ms ").format(int(counter * 100 / 44100 * 1000))  # *1000 to convert from sec to ms.


def raisingramp(data):
    data = data[::-1]
    counter = 0
    maksimumms=list()
    # plt.subplots(2,1)
    # plt.subplot(2,1,1)
    # plt.plot(data)
    data = [data[i * 10:(i + 1) * 10] for i in range(int(len(data) / 10))]
    for k, j in enumerate(data):
        ret = np.average(np.gradient(j))
        if ret < -0.5:
            maksimumms.extend(j)
    max = np.amax(maksimumms[:50])
    ret=np.argmax(maksimumms[:50])
    for i,j in enumerate(maksimumms):
        if i >ret and j<max*0.97:
            counter += 1
            if j<50:
                break
    # print("counter",counter)
    # plt.subplot(2, 1, 2)
    # plt.plot(maksimumms)
    # plt.title('raising ramp')
    # plt.show()
    return ("Raising ramp: {} ms ").format(int(counter * 100 / 44100 * 1000))  # *1000 to convert from sec to ms.
