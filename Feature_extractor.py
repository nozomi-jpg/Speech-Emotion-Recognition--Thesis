import numpy as np
import librosa
import parselmouth as praat
import math
import re

class feature_extractor:
    def __init__(self, AUDIO_PATH, FRAME_LENGTH, HOP_LENGTH):
        self.audio_path = AUDIO_PATH
        self.frame_length  = FRAME_LENGTH
        self.hop_length = HOP_LENGTH
        self.signal, self.sr = librosa.load(self.audio_path, sr=44100)
        self.sound = praat.Sound(self.audio_path)
        self.pitches, self.magnitudes = librosa.piptrack(y=self.signal, sr=self.sr)
        
    #ZERO-CROSSING RATE
    def get_zcr(self):
        zcr = librosa.feature.zero_crossing_rate(y=self.signal, frame_length=self.frame_length, hop_length=self.hop_length)
        return np.array([np.mean(zcr)])

    #MFCC
    def get_mfcc(self):
        mfcc = librosa.feature.mfcc(y=self.signal, sr=self.sr, n_mfcc=13, hop_length=self.hop_length)
        first_derivative_mfcc = librosa.feature.delta(mfcc, order=1)
        second_derivative_mfcc = librosa.feature.delta(mfcc, order=2)

        # aggregate MFCCs using mean
        mean_mfcc = np.mean(mfcc, axis=1)
        mean_fd_mfcc = np.mean(first_derivative_mfcc, axis=1)
        mean_sd_mfcc = np.mean(second_derivative_mfcc, axis=1)
        
        return np.array(mean_mfcc), np.array(mean_fd_mfcc), np.array(mean_sd_mfcc)

    #SPECTRAL CENTROID
    def get_spectral_centroid(self):
        spectral_centroid =  librosa.feature.spectral_centroid(y=self.signal, sr=self.sr, hop_length=self.hop_length)
        return np.array([np.mean(spectral_centroid)])

    #SPECTRAL BANDWIDTH
    def get_spectral_bandwidth(self):
        spectral_bandwidth =  librosa.feature.spectral_bandwidth(y=self.signal, sr=self.sr, hop_length=self.hop_length)
        return np.array([np.mean(spectral_bandwidth)])

    #ROOT MEAN SQUARE (RMS)
    def get_rms(self):
        rms = librosa.feature.rms(y=self.signal, hop_length=self.hop_length)
        return np.array([np.mean(rms)])

    #AMPLITUDE ENVELOPE
    def get_amplitude_envelope(self):
        amplitude_envelope = np.array([])
        for i in range(0, len(self.signal), self.hop_length):
            amplitude_envelope = np.append(
                amplitude_envelope, max(self.signal[i:i+self.frame_length]))
        return np.array([np.mean(amplitude_envelope)])

    #PITCH
    def get_pitch(self):
        pitch = np.array([])

        for t in range(self.pitches.shape[1]):
            pitch_frame = self.pitches[:, t]
            non_zero_pitches = pitch_frame[pitch_frame > 0]
            if non_zero_pitches.size > 0:
                pitch = np.append(pitch, non_zero_pitches[0])
            else:
                pitch = np.append(pitch, 0)

        return np.array([np.mean(pitch)])

    #FUNDAMENTAL FREQUENCY OF SPEECH (F0)
    def get_fundamental_frequency(self):
        f0_array = np.array([])

        for t in range(self.pitches.shape[1]):
            frequency_values = [self.sr / p for p in self.pitches[:, t] if p > 0]
            if len(frequency_values) > 0:
                average_frequency = sum(frequency_values) / len(frequency_values)
                f0_array = np.append(f0_array, np.mean(average_frequency))
            else:
                f0_array = np.append(f0_array, 0)
                
        return [f0_array, np.array([np.mean(f0_array)])]

    #HARMONIC TO NOISE RATIO
    def get_HNR(self):
        HarmonicToNoiseRatio = self.sound.to_harmonicity()
        HarmonicToNoiseRatio = HarmonicToNoiseRatio.values
        return np.array([np.mean(HarmonicToNoiseRatio)])
    

    #INHARMONICITY
    def get_inharmonicity(self, f0_array):
        inharmonicity = np.array([])
        highest_frequencies = np.array([])

        for i in range(0, len(self.signal), self.hop_length):

            #get the highest frequency for each frame
            frame_FFT = np.abs(np.fft.fft(self.signal[i:i+self.frame_length]))
            highest_freq_index = np.argmax(frame_FFT)
            highest_frequency = highest_freq_index / self.frame_length * self.sr
            highest_frequencies = np.append(highest_frequencies, highest_frequency)

        for i in range(len(highest_frequencies)):
            if(f0_array[i]!=0):
                inharmonicity = np.append(inharmonicity, highest_frequencies[i]/ f0_array[i] - math.floor(highest_frequencies[i]/ f0_array[i]))
            else:
                inharmonicity = np.append(inharmonicity,0)

        return np.array([np.sum(inharmonicity)])

    #FOR EXTRACTING ALL FEATURES
    def extract_all_features(self):

        zcr = self.get_zcr() #zero crossing rate
        amplitude_envelope = self.get_amplitude_envelope() #amplitude envelope
        f0 = self.get_fundamental_frequency()[1] #fundamental frequency
        hnr = self.get_HNR() #Harmonic Noise to Ratio
        pitch = self.get_pitch() #Pitch 
        spectral_bandwidth = self.get_spectral_bandwidth() #Spectral Bandwith
        spectral_centroid = self.get_spectral_centroid() #Spectral Centroid
        inharmonicity = self.get_inharmonicity(self.get_fundamental_frequency()[0]) #Inharmonicity
        mfcc = self.get_mfcc() #MFCC
        
        features = np.concatenate((zcr, amplitude_envelope, f0, hnr, pitch, spectral_bandwidth, spectral_centroid, inharmonicity, mfcc[0], mfcc[1], mfcc[2]))

        return features

