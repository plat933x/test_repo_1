import config
import control

import matplotlib.pyplot as plt

def Audio_mute(A_cut,B_cut=[]):
    if config.channel==1:
        # plt.plot(config.A_cut)
        # plt.title('mute ramp sample to analyze')
        # plt.show()
        mute_counter=0
        # print(len(config.A_cut))
        for i in A_cut[config.muteliveposition::]:
            if i!=0:
                ret=control.mag2db(abs(i))
            else:
                config.counter += 1
                continue
            if config.live_signal==1 and config.muteliveposition >= len(A_cut)-1:
                # print(config.muteliveposition)
                config.muteliveposition=0
                return config.linkpositions
            if ret < control.mag2db(config.mute_treshold):
                config.mutestate=True
                config.counter += 1
                config.reset=0
                config.muteliveposition + 1
                continue
            elif ret >= control.mag2db(config.mute_treshold) and mute_counter <= 4100:
                config.mutestate = False
                mute_counter+=1
                continue
            elif ret >= control.mag2db(config.mute_treshold) and config.reset == 0 and config.counter > 4100: # mute dluzszy niz 300 ms (4100 to 100 ms)
                config.mutestate = False
                config.mute_detect_samplingAudio = 1
                if config.live_signal == 1:
                    config.linkpositions.insert(0, f'{int((config.counter / config.fs) * 1000)}{"ms"}')
                    if len(config.linkpositions)>3:
                       config.linkpositions.pop()
                else:
                    config.mutestate=False
                    config.linkpositions.append("{} ms".format(int((config.counter / config.fs) * 1000)))
                mute_counter=0
                config.counter = 0
                config.reset=1
                config.muteliveposition + 1
                # if config.channel != 1:
                #     Audio_mute()
                continue
            else:
                config.mutestate = False
                mute_counter = 0
                config.counter=0
                config.muteliveposition + 1
                continue
        return config.linkpositions
    else:
        for i in [*A_cut[-20000:], *B_cut[:20000]]:
            if abs(i) < control.mag2db(config.mute_treshold):
                config.counter += 1
                if config.counter > 5000:#It is around 100 ms of mute state.
                    return "-1"
            else:
                config.counter = 0
    return "0"