from scipy.io import wavfile
import numpy as np
import winsound as ws
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fft import fft

class Soundfiles:
    def __init__(self,
                  Soundfile:str
                ):
        #Read in Soundfile
        self.SampleRate, self.Data = wavfile.read(Soundfile, 'r')
        self.NumberSamples =len(self.Data)
        # Reduce Stereo Signal to a Mono Signal (Average of both Channels)
        self.Data_Mono_Norm=np.sum(self.Data,axis=1)/2 

    def play(self):
        sd.play(self.Data_Mono_Norm, self.SampleRate)
   
    def plot(self):
        plt.plot(range(0,self.NumberSamples) ,self.Data)

    def get_FFTData (self):
        return fft(self.Data_Mono_Norm)
    



def main():
    EngineFaulty1= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty1.wav")
    EngineFaulty2= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty2.wav")
    EngineNominal= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineNominal.wav")
    EngineFaulty1.plot()
    #EngineFaulty1.play()


if __name__ == "__main__":
    main()