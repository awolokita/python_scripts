# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:30:59 2016

@author: Andre
"""

from ppfb_channeliser import ppfb_channeliser
from scipy.signal import chirp
import numpy as np
import matplotlib.pyplot as plt

fs = 16000
num_channels = 8
t = np.arange(0,10,1/fs)
#x = chirp(t,0,t[-1],fs/2)
x = np.cos(2*np.pi*4000*t)

s = ppfb_channeliser(fs, fs/2, 900, num_channels)
s.create_filter(0.8)
y = s.channelise(x)

plt.figure()
plt.specgram(x,NFFT=512,Fs=fs,noverlap=0)
for i in range(0,num_channels-1):
    plt.figure()
    plt.specgram(y[:,i],NFFT=512,Fs=s.get_output_fs(),noverlap=0)
    plt.figure()
    plt.plot(np.real(y[:,i]))
print('done')