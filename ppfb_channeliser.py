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

class ppfb_channeliser:
    
    def __init__(self, fs, input_bandwidth, channel_bandwidth,
                 num_channels):
        self.input_fs = fs
        self.num_channels = next_pow_2(num_channels)
        self.input_bandwidth = input_bandwidth
        self.channel_spacing = input_bandwidth/num_channels
        self.output_fs = self.channel_spacing
        self.channel_bandwidth = channel_bandwidth
        

    def create_filter(self, trans_alpha):
        # TODO: Check that len(taps)%num_channels = 0
        fs = self.input_fs
        norm = fs
        channel_bandwidth = self.channel_bandwidth
        num_channels = self.num_channels

#        trans_alpha = max(min(trans_alpha,1),0)
        
        cutoff = (channel_bandwidth/2)/norm
        trans = cutoff*0.2
        stop = cutoff+trans#(0.5 + cutoff)/2 # (trans_alpha/4)
        bands = [0, cutoff, stop, 0.5]
        taps = remez(512, bands, [1,0])
        
        # Break the FIR taps into num_channels number of filters and populate
        l = len(taps)
        m = self.num_channels
        n = int(l/m)
        self.polyphase_filter_bank = np.ndarray([m,n])
        for k in range(0,m-1):
            self.polyphase_filter_bank[k] = taps[k:(l-m+k+1):m]
        
        #w, h = freqz(taps)
        #plot_response(fs, w, h, "Low-pass Filter")
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
        channel_outputs = np.ndarray([len(x),M])
        
        # Zero pad the input signal
        z = L-np.mod(len(x),L)
        x = np.ravel(x)
        x = np.concatenate([x,np.ravel(np.zeros([1,z]))])
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
                path_line.appendleft(inputs[i])
                bank_output[i] = lfilter(path_filter,1,path_line)
            
            # Perform FFT stage of channeliser
            channel_outputs[k/M] = np.fft(bank_output,n=M)
        
        return channel_outputs
        
    def fir(x,taps):
        