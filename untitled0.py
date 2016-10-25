# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:30:59 2016

@author: Andre
"""

from ppfb_channeliser import ppfb_channeliser
from fsk import fsk

from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write




fs = 12288
in_bw = fs/2
ch_bw = 384
n_ch = 8

t = np.arange(0,10,1/fs)
x = chirp(t,0,t[-1],fs/2)
#scaled = np.int16(x/np.max(np.abs(x)) * 32767)
#write('test.wav', fs, scaled)
#x = np.cos(2*np.pi*4000*t)

ppfb = ppfb_channeliser(fs, in_bw, ch_bw, n_ch)

modem = fsk(fs=fs,fc=0,fdelta=0)

ppfb.create_filter(512)
y = ppfb.channelise(x)

plt.figure()
plt.specgram(x,NFFT=512,Fs=fs,noverlap=0)
for i in range(0,n_ch):
    plt.figure()
    plt.specgram(y[:,i],NFFT=128,Fs=ppfb.get_output_fs(),noverlap=0)
    plt.figure()
    plt.plot(y[:,i])
    name = 'ch_'+str(i)
    j = np.ravel(np.absolute(y[:,i]))
    scaled = np.int16(j/np.max(np.abs(j))* 32767)
    #print(y[:,i].shape)
    write(name, int(ppfb.get_output_fs()), scaled)
print('done')