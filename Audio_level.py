import config
import numpy as np
import control

def Audio_level(param,A_cut,B_cut=[]):
    if config.channel==1:
        try:
            ret = np.amax(A_cut)
            if ret == 0:
                return (f'{0}{"DB"}')
            decibelAmax = int(20 * np.log10(np.sqrt(np.mean(np.absolute(ret) ** 2)))) #for maksimum value <- this
            decibelAaverage = int(control.mag2db(np.average(np.abs(A_cut)))) # for average value <- this
            if decibelAaverage <= int(control.mag2db(config.mute_treshold)):
                return "Mute"
            else:
                return "{} DB max {} DB ".format(decibelAaverage,decibelAmax)
        except OverflowError:
            ret =  (f'{0}{"DB"}')
            if config.server_adress != 0:
                config.server_adress.send(bytes(str(ret)+'\r\n', encoding='utf-8'))
    else:
        if param == 1:
            A1 = A_cut[-88200:-10000]
            B1 = B_cut[10000:88200]
        else:
            A1 = A_cut[-88200:]
            B1 = B_cut[:88200]
        decibelAmax=int(20*np.log10(np.sqrt(np.mean(np.absolute(np.max(A1))**2))))
        decibelAaverage = int(control.mag2db(np.average(np.abs(A1))))
        decibelBmax=int(20*np.log10(np.sqrt(np.mean(np.absolute(np.max(B1))**2))))
        decibelBaverage = int(control.mag2db(np.average(np.abs(B1))))
        diff=np.absolute(decibelAaverage)-np.absolute(decibelBaverage)
        if diff >= 5:
            return "{} ,first average: {}DB max: {}DB second average: {}DB max: {}DB".format(-1,decibelAaverage,decibelAmax,decibelBaverage,decibelBmax)
        else:
            return "{} ,first average: {}DB max: {}DB second average: {}DB max: {}DB".format(0,decibelAaverage,decibelAmax,decibelBaverage,decibelBmax)
