import numpy as np
import config
from scipy.fftpack import irfft
from scipy.stats import kurtosis
from timeit import default_timer as timer
import matplotlib.pyplot as plt
def delay(data1,data2,q5):
    time_FFT_A = np.array([])
    time_FFT_B = np.array([])
    data1 = [(data1[i * 4410:(i + 1) * 4410]) for i in range(int(len(data1)/4410))]
    data2 = [(data2[i * 4410:(i + 1) * 4410]) for i in range(int(len(data2)/4410))]

    #for time, value in enumerate(data1):
    time_FFT_A = np.append(time_FFT_A, [irfft(data1[time]) for time, value in enumerate(data1)])
    time_FFT_B = np.append(time_FFT_B, [irfft(data2[time])for time, value in enumerate(data2)])

    corr = np.correlate(time_FFT_A, time_FFT_B, "full")
    maks = np.argmax(np.absolute(corr))
    if maks < 20000:
        sample2kurtosis = corr[:maks + 20000]
    else:
        sample2kurtosis = corr[maks - 20000:maks + 20000]
    kurtosiss = kurtosis(sample2kurtosis)
    match_counter = 0
    for x, j in enumerate(corr[maks - 5000:maks + 5000]):
        if x < 4900 or x > 5100:
            if j > np.amax(corr) * 0.30:
                match_counter +=1
    # print('Peaks: ',match_counter)
    # print('Przesunięcie =', np.argmax(corr) - (len(time_FFT_B) - 1))
    q5.put([kurtosiss,match_counter])
