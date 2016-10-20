import numpy as np
from scipy.signal import spectrogram

class fsk:
    
    def __init__(self):
        self.fs = 1000.0
        # Symbol period
        self.sym_t = 1
        # FSK centre frequency
        self.f_centre = 400
        # Symbol frequency deviation
        self.f_delta = 25
        # Time sample vector for generating symbol
        self.x = np.linspace(0.0,self.sym_t,self.sym_t*self.fs)

        q_sym_0 = np.cos(2*np.pi*(self.f_centre-self.f_delta)*self.x)
        i_sym_0 = 0
        q_sym_1 = np.cos(2*np.pi*(self.f_centre+self.f_delta)*self.x)
        i_sym_1 = 0
      
        self.fsk_map = { 
                         '0': (q_sym_0, i_sym_0),
                         '1': (q_sym_1, i_sym_1)
                       }

    def mod_bit(self, bit):
        i_vector = self.fsk_map[str(bit)][0]
        q_vector = self.fsk_map[str(bit)][1]      
        return i_vector + q_vector

    def mod(self, bit_string):
        bit_list = list(bit_string)
        signal = self.mod_bit(bit_list[0])
        bit_list = bit_list[1:]

        for bit in bit_list:
            signal = np.concatenate([signal, self.mod_bit(bit)])
        return signal
        
    def demod(self, signal, fs, channel_freqs, channel_width):
        nfft = 512
        bw = fs/nfft
        
        s = spectrogram(signal,fs,nfft=nfft,noverlap=100)
        #freq = s[0]
        
        channel_freqs.sort()
        w = channel_width/2
        channel_bands = dict()
        for f in channel_freqs:
            lb = round((f-w)/bw)
            cb = round(f/bw)
            ub = round((f+w)/bw)
            channel_bands[str(f)] = (lb,cb,ub)

        #time = s[1]
        spectrum = s[2]
        
        n = spectrum.shape[1]
        r = np.empty([1,n])
        b = channel_bands['10']
        for i in range(n):
            e_0 = sum(spectrum[b[0]:b[1]-1,i])
            e_1 = sum(spectrum[b[1]+1:b[2],i])
            r[0][i] = (e_1 - e_0)/(e_1 + e_0)
        return r[0]