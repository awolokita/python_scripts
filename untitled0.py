# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 21:30:59 2016

@author: Andre
"""

from ppfb_channeliser import ppfb_channeliser

s = ppfb_channeliser(10000, 5000, 1000, 2)
s.create_filter(0.8)