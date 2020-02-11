import time
from pydub import AudioSegment
def Audio_cuting(t2, path,time_cut=10000):
    t = time.localtime(time.time())
    newAudio1 = AudioSegment.from_wav(path)
    if (t2-time_cut)<0:
        newAudio1 = newAudio1[0:t2]
    else:
        newAudio1 = newAudio1[t2 - time_cut:t2]
    path1 = 'C:/YA_MIB3/logs/audio/audio_cut/{}_1.wav'.format(time.strftime("%d-%m-%y_%H-%M-%S", t))
    newAudio1.export(path1, format="wav")
    newAudio2 = AudioSegment.from_wav(path)
    newAudio2 = newAudio2[t2:t2 + time_cut]  # milisec
    path2 = 'C:/YA_MIB3/logs/audio/audio_cut/{}_2.wav'.format(time.strftime("%d-%m-%y_%H-%M-%S", t))
    newAudio2.export(path2, format="wav")
    return(path1, path2)
