# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:30:59 2016

@author: Andre
"""

from ppfb_channeliser import ppfb_channeliser
from fsk import fsk
import matplotlib.pyplot as plt
from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import buttord
from scipy.signal import cheb1ord
from scipy.signal import butter
from scipy.signal import freqz

plot_figures = 0


fs = 100000000
in_bw = fs/2
n_ch = 20
ch_bw = in_bw/n_ch
wp = ((in_bw/2)-(ch_bw/2))
ws = (in_bw/2)
#wp = 100000
#ws = 150000

bit_stream = '1010101010101010101010'

#t = np.arange(0,10,1/fs)
#x = chirp(t,0,t[-1],fs/2)
#scaled = np.int16(x/np.max(np.abs(x)) * 32767)
#write('test.wav', fs, scaled)
#x = np.cos(2*np.pi*4000*t)

[n,wn] = buttord(wp/fs,ws/fs,1.5,80,False)
#b, a = butter(n, wn, 'lowpass', False)
#w, h = freqz(b,a)
#plt.figure()
#plt.plot(w, 20 * np.log10(abs(h)))
print(n)
n =  cheb1ord(wp/fs,ws/fs,1.5,80,False)
print(n)

#ppfb = ppfb_channeliser(fs, in_bw, ch_bw, n_ch)
#ppfb.create_filter(4000)

#fc = ppfb.get_channel_centres()[(n_ch/2+1)+0]
#print(fc)
#modem1 = fsk(fs=fs,fc=fc,fdelta=ch_bw/2)
#fc = ppfb.get_channel_centres()[(n_ch/2+1)+1]
#print(fc)
#modem2 = fsk(fs=fs,fc=fc,fdelta=ch_bw/2)
#fc = ppfb.get_channel_centres()[(n_ch/2+1)+2]
#print(fc)
#modem3 = fsk(fs=fs,fc=fc,fdelta=ch_bw/2)

#mod_stream1 = modem1.mod('101010101010101010101010')
#mod_stream2 = modem2.mod('110011001100110011001100')
#mod_stream3 = modem3.mod('111100001111000011110000')

#mod_stream = mod_stream1+mod_stream2+mod_stream3

#plt.figure()
#plt.specgram(mod_stream,NFFT=128,Fs=fs,noverlap=0)

#y = ppfb.channelise(mod_stream)


if (plot_figures == 1):
    for i in range(0,int(n_ch/2)):
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