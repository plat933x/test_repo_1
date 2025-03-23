import Audio_level
import Correlation
import config
from scipy.io.wavfile import read
import threading
import multiprocessing
import socket, re, sys

def server():
    sock = socket.socket()
    sock.bind(('',54321))
    sock.listen(5)

    config.server_adress, addr = sock.accept()

def Audio_analyzer(args):

    threading.Thread(target=server, args=()).start()

    if args[1].lower() == "live":  # live signal analysis
        config.live_signal = 1
        config.channel = 1
        threading.Thread(target=Record.Record, args=(args[1],'',float(args[2]))).start()  # Thread to start live signal record
        while True:
            if config.server_adress == 0:
                continue
            else:
                a = config.server_adress.recv(10)
                break
        if re.search("stop",str(a)):
            config.stream.stop_stream()
            config.stream.close()
        return 0
    elif args[1].lower() == "record_on_demand":  # Record on Demand
        config.live_signal = 1
        config.channel = 1
        if len(args) == 4:
            t1=threading.Thread(target=Record.Record, args=(args[1],args[2],int(args[3]),0)).start()
        else:
            t1=threading.Thread(target=Record.Record, args=(args[1],args[2],int(args[3]),int(args[4]))).start()  # Thread to start live signal record
        while True:
            if config.server_adress == 0:
                continue
            else:
                a = config.server_adress.recv(10)
                break
        if re.search("stop",str(a)):
            config.stop_request=1
        elif re.search("end",str(a)):
            config.stop_request=2
        return 0
    elif args[1].lower() == "link_test":
        Link_recognizer.linkdetection()
    elif len(args) == 2:  # only one file to analyse
        config.channel = 1
        config.fs, A_cut = read(args[1], mmap=True)
        A_cut = A_cut[20000:] # Cut first 20000 samples because of mute state at beginning of the file
        multiprocessing.Process(target=Sampling_Audio.Sampling_Audio,
                              args=(A_cut,)).run()  # Threat to count mute and demute ramp
        mute_result = ', '.join(Audio_mute.Audio_mute(A_cut))
        if mute_result == "-1":
            audiolevel_result = Audio_level.Audio_level(1,A_cut)
        else:
            audiolevel_result = Audio_level.Audio_level(0,A_cut)
        ret = ("Audio level {} Audio Mute {}".format(audiolevel_result,
                                                                 mute_result))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))
        return ("Audio level {} Audio Mute {}".format(audiolevel_result,
                                                                   mute_result))
    elif isinstance(args[2], int) == True and args[2] != -1:  # only one wav file and position where file should be cut
        result = Audio_cuting.Audio_cuting(args[2], args[1])
        config.fs, A = read(result[0], mmap=True)
        fs_2, B = read(result[1], mmap=True)
        config.channel = 2
        _n0_sample=int(config._Time_to_Analyze_*config.fs)
        A_cut = A[-_n0_sample:]  # last x second of data to analyze
        B_cut = B[:_n0_sample]   # first x second of data to analyze
    else:   # two file to analyze
        # print("elo")
        config.fs, A = read(args[1], mmap=True)
        fs_2, B = read(args[2], mmap=True)
        config.channel = 2
        _n0_sample = int(config._Time_to_Analyze_ *config.fs)
        A_cut = A[-_n0_sample:]  # last x second of data to analyze
        B_cut = B[:_n0_sample]   # first x second of data to analyze

    q5=multiprocessing.Queue()
    multiprocessing.Process(target=Correlation.delay, args=(A_cut,B_cut,q5)).start()
    Sampling_Audio.Sampling_Audio([*A_cut, *B_cut],) # Threat to count mute and demute ramp

    mute_result =Audio_mute.Audio_mute(A_cut,B_cut)
    if mute_result == "-1":
        audiolevel_result = Audio_level.Audio_level(1,A_cut,B_cut)
    else:
        audiolevel_result = Audio_level.Audio_level(0,A_cut,B_cut)
    ___corelation_result___=q5.get()
    if ___corelation_result___ == -1:
        ret = (
            "Audio wasn't repeated in those samples. Number of peaks: {} kurtosis {} Audio level {} Audio Mute {}".format(
                ___corelation_result___[1], ___corelation_result___[0], audiolevel_result,mute_result))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))
        return (
            "Audio wasn't repeated in those samples. Number of peaks: {} kurtosis {} Audio level {} Audio Mute {}".format(
                ___corelation_result___[1], ___corelation_result___[0], audiolevel_result,mute_result))
    else:
        ret = ("Audio Repeated kurtosis {} Number of peaks: {} Audio level {} Audio Mute {}".format(
            ___corelation_result___[0], ___corelation_result___[1], audiolevel_result,mute_result))
        if config.server_adress != 0:
            config.server_adress.send(bytes(str(ret) + '\r\n', encoding='utf-8'))
        return (
        "Audio Repeated kurtosis {} Number of peaks: {} Audio level {} Audio Mute {}".format(
            ___corelation_result___[0], ___corelation_result___[1], audiolevel_result,mute_result))


if __name__ == "__main__":
    # lista = [0, 'live','0.5'] # Live signal| second parameter is the time how often u want receive result
    lista = [0, 'record_on_demand','C:/','5','5']  # Record on Demand | second parameter is total time of file
    # lista = [0, 'C:/YA_MIB3/logs/audio/record_demand/2020-01-14__07-59-20.wav',2000]
    # lista = [0, 'C:/YA_MIB3/logs/audio/record_demand/2020-01-14__07-59-20.wav','C:/YA_MIB3/logs/audio/record_demand/2020-01-14__07-59-20.wav']
    Audio_analyzer(sys.argv)
