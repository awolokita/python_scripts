#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 10:43:26 2016

@author: awolokit
"""

from fsk import fsk
from ddc import ddc
import numpy as np
import matplotlib.pyplot as plt

modem = fsk()
ddc = ddc(modem.fs,modem.f_centre,modem.f_delta*2.0)
bit_stream = '10101010'

mod_stream = modem.mod(bit_stream)

r = modem.demod(mod_stream,modem.fs,[10],20)

ddc_I, ddc_Q = ddc.process(mod_stream)
s = ddc_I + ddc_Q

#plt.plot(r)
#plt.plot(X,np.abs(Y))
#plt.axis([-20,20,0,2500])
plt.figure()
plt.specgram(mod_stream,NFFT=512,Fs=modem.fs,noverlap=0)
plt.figure()
plt.specgram(ddc_I,NFFT=128,Fs=ddc.fs_out,noverlap=0)
plt.figure()
plt.specgram(ddc_Q,NFFT=128,Fs=ddc.fs_out,noverlap=0)
#plt.figure()
plt.figure()
plt.specgram(ddc_I-ddc_Q,NFFT=128,Fs=ddc.fs_out,noverlap=0)
#plt.figure()

#spectrum = s[0]
#n = spectrum.shape[1]
#r = np.empty([1,n])
#for i in range(n):
#    e_0 = sum(spectrum[2:4,i])
#    e_1 = sum(spectrum[7:9,i])
#    
#    r[0][i] = (e_1 - e_0)/(e_1 + e_0)
#    
#for i in range(1,n):
#    dr = abs(round(r[0][i]-r[0][i-1]))
#    print(dr)