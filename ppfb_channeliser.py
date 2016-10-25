# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 19:22:41 2016

@author: Andre
"""

import numpy as np
import math
from scipy.signal import remez
from scipy.signal import lfilter
from scipy.signal import chirp
from scipy.signal import freqz
import matplotlib.pyplot as plt
from collections import deque

def next_pow_2(x):
    return 1<<(x-1).bit_length()

def plot_response(fs, w, h, title):
    plt.figure()
    plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-140, 5)
    plt.xlim(0, 0.5*fs)
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.title(title)

def fir(x,taps):
    y = np.multiply(x,taps)
    y = np.sum(y)
    return y
    
class ppfb_channeliser:
    
    def __init__(self, fs, input_bandwidth, channel_bandwidth,
                 num_channels):
        self.input_fs = fs
        self.num_channels = next_pow_2(num_channels)
        self.input_bandwidth = input_bandwidth
        self.channel_spacing = fs/num_channels
        self.output_fs = self.channel_spacing
        self.channel_bandwidth = channel_bandwidth
        self.alpha = 1.0
        self.channel_centres = np.linspace(-fs/2,fs/2,num=9)
        print(self.channel_centres)
        
    def create_filter(self, n_taps):
        # TODO: Check that len(taps)%num_channels = 0
        fs = self.input_fs
        channel_bandwidth = self.channel_bandwidth
        
        cutoff = channel_bandwidth/fs
        stop = self.alpha*self.channel_spacing/fs
        stop = min(max(cutoff,stop),0.45)
        stop = cutoff+(cutoff*0.25)
        bands = [0, cutoff, stop, 0.5]
        print(bands)
        taps = remez(n_taps, bands, [1,0])
        
        # Break the FIR taps into num_channels number of filters and populate
        l = len(taps)
        m = self.num_channels
        n = int(l/m)
        self.polyphase_filter_bank = np.ndarray([m,n])
        for k in range(0,m):
            self.polyphase_filter_bank[k] = taps[k:(l-m+k+1):m]
        
        w, h = freqz(taps)
        plot_response(fs, w, h, "Low-pass Filter")
        #t = np.arange(0,10,1/fs)
        #x = chirp(t,0,t[-1],norm/2)
        #y = lfilter(taps,1,x)
        #plt.figure()
        #plt.specgram(x,NFFT=512,Fs=fs,noverlap=0)
        #plt.figure()
        #plt.specgram(y,NFFT=512,Fs=fs,noverlap=0)
        
    def channelise(self,x):
        L = self.polyphase_filter_bank.size
        M = self.num_channels
        N = int(L/M)
        delay_lines = list()
        bank_output = np.ravel(np.zeros([1,M]))
        
        # Zero pad the input signal
        z = L-np.mod(len(x),L)
        x = np.ravel(x)
        x = np.concatenate([x,np.ravel(np.zeros([1,z]))])
        channel_outputs = np.ndarray([np.int32(len(x)/M),M],dtype='complex')
        #x = np.reshape(x, [-1,L])
        
        #  Create an array of circular buffers
        for i in range(0,M):
            delay_lines.append(deque(np.ravel(np.zeros([1,N])).tolist(),maxlen=N))
        
        for k in range(0,len(x),M):
            inputs = x[k:k+M]
            # Push inputs into delay lines and process new outputs
            for i in range(0,len(inputs)):
                path_filter = self.polyphase_filter_bank[i]
                path_line = delay_lines[i]
                path_line.append(inputs[i])
                #bank_output[i] = lfilter(path_filter,1,path_line)
                bank_output[i] = fir(path_line,path_filter)
            
            # Perform FFT stage of channeliser
            channel_outputs[int(k/M)] = np.fft.fft(bank_output,n=M)
#            if(k == 520):
 #               print('foo')
        return channel_outputs
        
    def get_output_fs(self):
        return self.output_fs