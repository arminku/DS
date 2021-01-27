import numpy as np
import winsound as ws
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.fft import fft
from sklearn.preprocessing import scale

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
        plt.show()

    def get_Data_Raw(self):
        return self.Data
    
    def get_Data_Mono(self):
        return np.sum(self.Data,axis=1)/2 
    
    def get_Data_Mono_Normalized(self):
        return scale(self.get_Data_Mono(),)

    def get_Data_FFT (self):
        return fft(self.Data_Mono_Norm)
    



def main():
    EngineFaulty1= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty1.wav")
    EngineFaulty2= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty2.wav")
    EngineNominal= Soundfiles("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineNominal.wav")
    t=np.linspace(0,  EngineFaulty1.NumberSamples/EngineFaulty1.SampleRate, EngineFaulty1.NumberSamples)
    plt.plot(t,EngineFaulty1.get_Data_Mono_Normalized())
    plt.xlim(0,1)
    plt.show()
    #EngineFaulty1.play()


if __name__ == "__main__":
    main()
    #VSC TF
    # use conda install -c conda-forge python-sounddevice