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
        fs = self.input_fs
        norm = fs
        channel_bandwidth = self.channel_bandwidth

        trans_alpha = max(min(trans_alpha,1),0)
        
        cutoff = (channel_bandwidth/2)/norm
        trans = cutoff*0.2
        stop = cutoff+trans#(0.5 + cutoff)/2 # (trans_alpha/4)
        bands = [0, cutoff, stop, 0.5]
        self.filter = remez(512, bands, [1,0])
        w, h = freqz(self.filter)
        plot_response(fs, w, h, "Low-pass Filter")
        t = np.arange(0,10,1/fs)
        x = chirp(t,0,t[-1],norm/2)
        y = lfilter(self.filter,1,x)
        plt.figure()
        plt.specgram(x,NFFT=512,Fs=fs,noverlap=0)
        plt.figure()
        plt.specgram(y,NFFT=512,Fs=fs,noverlap=0)
        