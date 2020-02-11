import pyaudio
import struct
import config
import Audio_level
import Audio_mute
import Sampling_Audio
import wave
import os
import timeit
import threading
import Context_check
from datetime import datetime

def Record (in_value,path,duration,duration1=0):
    bits = 16
    config.fs = 44100
    channels = 1
    #chunk = 1024  # Record in chunks of 1024 samples
    if bits == 16:
        sample_format = pyaudio.paInt16  # 16 bits per sample
    elif bits == 24:
        sample_format = pyaudio.paInt24  # 24 bits per sample
    elif bits == 32:
        sample_format = pyaudio.paInt32  # 32 bits per sample
    elif bits == 8:
        sample_format = pyaudio.paInt8  # 8 bits per sample
    else:
        return "Wrong bits it can be: 8, 16, 24, 32"
    if channels > 2:
        return "Wrong channels it can be: 1, 2"

    if in_value.lower() == 'live':
        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        chunk=int(44100*duration)
        def callback(in_data, frame_count, time_info, status):
            if config.beg_counter==0:
                config.beg_counter=1
                return (in_data,0)
            A_cut=struct.unpack("%dh"%(len(in_data)/2),in_data)
            Sampling_Audio.Sampling_Audio(A_cut, chunk)
            pyaudio.paContinue
            ret = (Audio_level.Audio_level(0,A_cut)), ', '.join(Audio_mute.Audio_mute(A_cut))

            if config.server_adress != 0:
                config.server_adress.send(bytes(str(ret)+'\r\n', encoding='utf-8'))
            return (in_data,0)

        config.stream = p.open(format=sample_format,
                               channels=channels,
                               rate=config.fs,
                               frames_per_buffer=chunk,# bylo chunk - config.fs give 1 sec iteration between print of audio lvl on live signal
                               input=True,
                               stream_callback=callback)
        config.stream.start_stream()

        return 0

    elif in_value.lower() == 'record_on_demand':
        threading.Thread(target=Context_check.start_web_driver, args=()).start()
        if duration1 == 0:
            maxcounter = duration/2
            counter = duration/2
        else:
            maxcounter = duration1
            counter = duration1
        chunk = 44100
        __data_container__ = []
        p = pyaudio.PyAudio()
        config.stream = p.open(format=sample_format,
                                   channels=channels,
                                   rate=config.fs,
                                   frames_per_buffer=chunk,# bylo chunk - config.fs give 1 sec iteration between print of audio lvl on live signal
                                   input=True)
        config.start_time = timeit.default_timer()
        config.stream.start_stream()

        while config.stream.is_active():
            lenght=len(__data_container__)
            if config.stop_request==2:
                config.server_adress.send(bytes(str('end: request') + '\r\n', encoding='utf-8'))
                config.server_adress.close()
                config.driver.quit()
                return 0
            elif config.stop_request==1:
                if counter == maxcounter:
                    config._recordondemand_path_='{}/{:%Y-%m-%d_%H-%M-%S}'.format(path,datetime.today())
                    os.mkdir(config._recordondemand_path_)
                    threading.Thread(target=Context_check.Get_screenshoot, args=(config._recordondemand_path_,)).start()
                counter-=1
                if counter ==0:
                    config.stream.stop_stream()
                    config.stream.close()
                    break
                if lenght<duration+duration1:
                    __data_container__.append(config.stream.read(chunk))
                else:
                    __data_container__.pop(0)
                    __data_container__.append(config.stream.read(chunk))
            elif lenght<duration:
                __data_container__.append(config.stream.read(chunk))
            elif lenght==duration:
                __data_container__.append(config.stream.read(chunk))
                __data_container__.pop(0)
        filename='{}/{:%Y-%m-%d__%H-%M-%S}.wav'.format(config._recordondemand_path_,datetime.today())
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(config.fs)
        for i,j in enumerate(__data_container__):
            wf.writeframes(j)
        wf.close()


