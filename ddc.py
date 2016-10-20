# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 13:00:50 2016

@author: Andre
"""
import numpy as np
from scipy.signal import butter, lfilter, freqz
import math
import matplotlib.pyplot as plt

class ddc:
    def __init__(self, fs, fc, bp_width):
        cutoff = bp_width / (0.5 * fs)
        high = (fc + (bp_width/2))/ (0.5 * fs)
        low = (fc - (bp_width/2))/ (0.5 * fs)
        b, a = butter(10, [low,high], btype='band', analog=False)
        self.lp_b = b
        self.lp_a = a
        self.deci_factor = math.floor(fs/(bp_width * 2))
        self.fs = fs
        self.fc = fc
        self.fs_out = self.fs/self.deci_factor
        
    def process(self, signal):
        Ts = 1.0/self.fs
        Wc = 2 * np.pi * self.fc
        signal_length = len(signal)
        #t = np.linspace(0.0, signal_length/self.fs, signal_length)
        n = np.arange(0,signal_length,1)
        
        # Quadrature signals
        #I = np.cos(Wc*t)
        I = np.cos(2*np.pi*(n*self.fc/self.fs))
        Q = np.sin(2*np.pi*(n*self.fc/self.fs))
        
        # Mix quadrature signals with input
        mix_I = np.multiply(signal, I)
        mix_Q = np.multiply(signal, Q)
        
        # Lowpass mixed quadratures
        lp_I = lfilter(self.lp_b, self.lp_a, mix_I)
        lp_Q = lfilter(self.lp_b, self.lp_a, mix_Q)
        
        # Decimate
        deci_I = lp_I[0::self.deci_factor]
        deci_Q = lp_Q[0::self.deci_factor]
        return (mix_I, mix_Q)
        #return (lp_I, lp_Q)
        #return (deci_I, deci_Q)