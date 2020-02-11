import config
import numpy as np
import Mute_ramp
import threading
import control


import multiprocessing
import matplotlib.pyplot as plt
def Sampling_Audio(A_cut,chunk=22050):
    A1 = np.abs(A_cut)
    if chunk >=132300:
        __sample_lenght_=1
    else:
        __sample_lenght_=int((44100*3)/chunk) # set 3 sec of sampling to mute ramp in depend of chunk sizeof
    samples=[A1[i * chunk:(i + 1) * chunk] for i in range(int(len(A1) / chunk))]
    for i,j in enumerate(samples):
        length = len(config.samples_to_muteramp_analyze)
        if length > 300*(44100/chunk):
            config.counter_sampling[1] = __sample_lenght_
            config.samples_to_muteramp_analyze = []
            config.mute_detect_samplingAudio = 0
            continue
        ret = sine_detect(j, chunk)
        if length ==0:
            if ret == -2:
                config.samples_to_muteramp_analyze = []
                continue
                # return -2
            config.samples_to_muteramp_analyze.append([j, ret])
            config.counter_sampling[1] = __sample_lenght_
            config.counter_sampling[0]=ret
            continue
            # return 0
        elif length<__sample_lenght_ and config.mute_detect_samplingAudio==1: # reset sampling because mute occure before enough of sample data
            config.counter_sampling[1] = __sample_lenght_
            config.samples_to_muteramp_analyze = []
            config.mute_detect_samplingAudio = 0
        elif length<__sample_lenght_: # data to count mute ramp not enough so add another sample
            if ret == -2:
                config.samples_to_muteramp_analyze = []
                continue
                # return -2
            elif len(config.samples_to_muteramp_analyze)<__sample_lenght_:
                config.samples_to_muteramp_analyze.append([j, ret])
                config.counter_sampling[0]=ret
                continue
                # return 0
        else:
            if  config.counter_sampling[0]==ret and config.mute_detect_samplingAudio == 0: # append sample while the same kind of signal active
                config.samples_to_muteramp_analyze.append([j, ret])
                config.samples_to_muteramp_analyze.pop(0)
                continue
                # return 0
            elif ret == -2: #append sample because of mute ramp is present
                config.mute_detect_samplingAudio =1 # signal that mute occure (change station or mute occure)
                config.samples_to_muteramp_analyze.append([j, ret])
                continue
                # return 0
            elif config.samples_to_muteramp_analyze[__sample_lenght_-1][1]!=ret and ret != -2 and config.mute_detect_samplingAudio ==1:
                #signal is different than before mute state and add __sample_lenght_-1 more sample
                if config.counter_sampling[1]>0:
                    config.samples_to_muteramp_analyze.append([j, ret])
                    config.counter_sampling[1] -=1
                if config.counter_sampling[1] == 0: #last sample added and sample send to Mute ramp analyze, reset couters and containers
                    config.samples_to_muteramp_analyze.append([j, ret])
                    config.counter_sampling[1]=__sample_lenght_ # restore setting to default
                    samples_to_muteramp_analyze = config.samples_to_muteramp_analyze
                    multiprocessing.Process(target=Mute_ramp.mute_ramp,args=(samples_to_muteramp_analyze,)).run()
                    # threading.Thread(target=Mute_ramp.mute_ramp,args=(samples_to_muteramp_analyze,)).start()
                    config.samples_to_muteramp_analyze=[] # clean buffer to receive next sample for mute ramp measurement
                    config.mute_detect_samplingAudio = 0
                    continue
                    # return 1
            elif config.samples_to_muteramp_analyze[__sample_lenght_-1][1]==ret and ret != -2 and config.mute_detect_samplingAudio == 1:
                #Signal the same like before mute state, reset all counters and containers. except sine wave before and after
                if config.samples_to_muteramp_analyze[__sample_lenght_-1][1]==0:
                    if config.counter_sampling[1] > 0:
                        config.samples_to_muteramp_analyze.append([j, ret])
                        config.counter_sampling[1] -= 1
                    if config.counter_sampling[1] == 0:  # last sample added and sample send to Mute ramp analyze, reset couters and containers
                        config.samples_to_muteramp_analyze.append([j, ret])
                        config.counter_sampling[1] = __sample_lenght_  # restore setting to default
                        samples_to_muteramp_analyze = config.samples_to_muteramp_analyze
                        multiprocessing.Process(target=Mute_ramp.mute_ramp, args=(samples_to_muteramp_analyze,)).run()
                        # threading.Thread(target=Mute_ramp.mute_ramp, args=(samples_to_muteramp_analyze,)).start()
                        config.samples_to_muteramp_analyze = []  # clean buffer to receive next sample for mute ramp measurement
                        config.mute_detect_samplingAudio = 0
                        continue
                        # return 1
                else:
                    config.counter_sampling[1] = __sample_lenght_
                    config.samples_to_muteramp_analyze = []
                    config.mute_detect_samplingAudio = 0
            elif ret==-2:
                config.counter_sampling[1] = __sample_lenght_
                config.samples_to_muteramp_analyze = []
                config.mute_detect_samplingAudio = 0
        return 0

def sine_detect(sample,chunk):
   counter=0
   boundary_value=(1200*chunk)/22050
   if config.live_signal != 1:
       for i in sample:
           if abs(i) < control.mag2db(config.mute_treshold):
               counter += 1
               if counter > 5000:  # It is around 100 ms of mute state.
                   config.mute_detect_samplingAudio=1
                   return -2
   fft = np.abs(np.fft.fft(sample))
   average = np.average(fft)
   counter = 0
   for i, j in enumerate(fft):  # i pozycja aktualne, j to wartosc
       if i > len(fft) / 2:
           break
       if j > average:
           counter = counter + 1
           continue
   if counter > boundary_value:
       return -1
   return 0