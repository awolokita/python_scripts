# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:30:59 2016

@author: Andre
"""

from ppfb_channeliser import ppfb_channeliser
from scipy.signal import chirp
import numpy as np

fs = 10000
t = np.arange(0,10,1/fs)
x = chirp(t,0,t[-1],fs/2)

s = ppfb_channeliser(fs, 5000, 1000, 4)
s.create_filter(0.8)
y = s.channelise(x)