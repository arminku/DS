import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.fft import rfft
from scipy.fft import rfftfreq
from scipy import signal

class Soundfile:
    def __init__(self, Soundfile:str, Title, Color):
        #Read in Soundfile
        self.SampleRate, self.Data = wavfile.read(Soundfile, 'r')
        self.NumberSamples = len(self.Data)
        self.Title= Title
        self.Color=Color
        # Reduce Stereo Signal to a Mono Signal (Average of both Channels)
        self.Data_Mono = np.sum(self.Data,axis=1)/2 
        self.Data_Mono_Norm = self.Data_Mono/ abs(max(self.Data_Mono))
        self.X=np.linspace(0, (self.NumberSamples/self.SampleRate), self.NumberSamples)

        self.Data_FFT = abs(rfft(self.Data_Mono_Norm/self.NumberSamples))
        self.X_FFT= rfftfreq(len(self.Data_Mono_Norm), 1/self.SampleRate)
        self.sg_spectrum=None
        self.sg_frequencies=None
        self.sg_times=None

    def play(self):
        sd.play(self.Data_Mono_Norm, self.SampleRate)
    
    def subplot_Data_Norm(self, pltIdx, StartValue, EndValue, combined):  
        if not combined:     
            plt.subplot(3, 1, pltIdx)
            plt.ylabel('x(t)',size='medium')
            plt.plot(self.X, self.Data_Mono_Norm,c= self.Color,linewidth=0.5 )
            plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', linewidth=0.5)
            plt.title('Rohdaten '+ self.Title,fontweight='bold',size='medium')
            plt.xlim(StartValue,EndValue)
        else:
            plt.plot( self.X, self.Data_Mono_Norm,c= self.Color, alpha=0.5,linewidth=0.5)
    
    def subplot_Data_FFT(self, pltIdx, StartValue_X, EndValue_X,StartValue_Y,EndValue_Y, combined ):
        if not combined: 
            plt.subplot(3, 1, pltIdx)
            plt.ylabel('|X|',size='medium')
            plt.plot(self.X_FFT, self.Data_FFT,c= self.Color,linewidth=0.5)
            plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', linewidth=0.5)
            plt.title('Betragsspektrum '+ self.Title+ ' im Bereich von {}-{}Hz'.format(StartValue_X,StartValue_Y),fontweight='bold',size='medium')
            plt.xlim(StartValue_X, EndValue_X)
            plt.ylim(StartValue_Y, EndValue_Y)
        else:
            plt.plot( self.X_FFT, self.Data_FFT,c= self.Color, alpha=0.5,linewidth=0.5)

    def subplot_Data_FFT_Dif(self, pltIdx, StartValue, EndValue, Data):
        plt.subplot(2, 1, pltIdx)
        plt.ylabel('|X|',size='medium')
        plt.title('Störfrequenzen bei '+ self.Title+ ' im Bereich von {}-{}Hz'.format(StartValue,EndValue),fontweight='bold',size='medium')
        plt.plot(self.X_FFT, self.Data_FFT-Data,c= self.Color, linewidth=0.5)
        plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', lw=0.5)
        plt.xlim(StartValue, EndValue)

    def subplot_Spectrogram(self, pltIdx, StartValue, EndValue, Data):       
        plt.subplot(2, 1, pltIdx)
        self.sg_spectrum , self.sg_frequencies, self.sg_times,self.sg_im= plt.specgram((self.Data_Mono_Norm-Data), NFFT=4096, Fs=self.SampleRate, noverlap=1024,scale='dB', cmap='plasma')
        plt.ylim(StartValue,EndValue) 
        plt.title("Spektrogramm im Frequenzbereich {}-{}Hz".format(StartValue,EndValue),fontweight='bold',size='medium')
        plt.xlabel('Zeit [s]',size='small')
        plt.ylabel('Frequenz [Hz]',size='small')
       

def plotData (Soundfiles, StartValue, EndValue, combined):    #plot Data
    if not combined:
        fig, axs = plt.subplots(3, figsize=(10, 6), facecolor='#dddddd')
        Soundfiles[0].subplot_Data_Norm(1,StartValue,EndValue, combined)
        Soundfiles[1].subplot_Data_Norm(2,StartValue,EndValue, combined)
        Soundfiles[2].subplot_Data_Norm(3,StartValue,EndValue, combined) 
        plt.xlabel('Zeit [s]',size='medium')
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        plt.show()
    else:
        fig=plt.figure(figsize=(10, 4), facecolor='#dddddd')
        Soundfiles[0].subplot_Data_Norm(1,StartValue,EndValue, combined)
        Soundfiles[1].subplot_Data_Norm(2,StartValue,EndValue, combined)
        Soundfiles[2].subplot_Data_Norm(3,StartValue,EndValue, combined) 
        plt.xlabel('Zeit [s]',size='medium')
        plt.ylabel('x(t)',size='medium')
        plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', lw=0.5)
        plt.title('Rohdaten Signale kombiniert',fontweight='bold',size='medium')
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        plt.xlim(StartValue, EndValue)
        plt.show()


def plotDataFFT (Soundfiles,StartValue_X, EndValue_X,StartValue_Y,EndValue_Y, combined):    #plot Data
    if not combined:
        fig, axs = plt.subplots(3, figsize=(10, 6), facecolor='#dddddd')
        Soundfiles[0].subplot_Data_FFT(1,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined)
        Soundfiles[1].subplot_Data_FFT(2,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined)
        Soundfiles[2].subplot_Data_FFT(3,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined)
        plt.xlabel('Frequenz [Hz]',size='medium')
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        plt.show()
    else:
        fig=plt.figure(figsize=(10, 4), facecolor='#dddddd')
        Soundfiles[0].subplot_Data_FFT(1,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined)
        Soundfiles[1].subplot_Data_FFT(2,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined)
        Soundfiles[2].subplot_Data_FFT(3,StartValue_X,EndValue_X,StartValue_Y,EndValue_Y, combined) 
        plt.xlabel('Frequenz [Hz]',size='medium')
        plt.ylabel('|X|',size='medium')
        plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', linewidth=0.5)
        plt.title('Betragsspektrum Signale kombiniert',fontweight='bold',size='medium')
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)
        plt.xlim(StartValue_X, EndValue_X)
        plt.ylim(StartValue_Y, EndValue_Y)
        plt.show()

def plotDataFFT_diff(Soundfiles,StartValue, EndValue):
    fig, axs = plt.subplots(2, figsize=(10, 5), facecolor='#dddddd')
    Soundfiles[0].subplot_Data_FFT_Dif(1,StartValue,EndValue,Soundfiles[2].Data_FFT)
    Soundfiles[1].subplot_Data_FFT_Dif(2,StartValue,EndValue,Soundfiles[2].Data_FFT)
    plt.xlabel('Frequenz [Hz]',size='medium')
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    plt.show()

def plot_Spectrogram(Soundfiles,StartValue, EndValue):   
    fig, axs = plt.subplots(2, figsize=( 10,6), facecolor='#dddddd')
    Soundfiles[0].subplot_Spectrogram(1,StartValue,EndValue,Soundfiles[2].Data_Mono_Norm)   
    plt.colorbar().set_label('Intensität [dB/Hz]', size='medium')
    Soundfiles[1].subplot_Spectrogram(2,StartValue,EndValue,Soundfiles[2].Data_Mono_Norm)   
    plt.colorbar().set_label('Intensität [dB/Hz]', size='medium') 
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    plt.show()

def plot_amplitude_maxfreq(SoundfileEngine2:Soundfile,SoundfileNominal:Soundfile):
    # get coordinates of highest amplitude in spectrum  
    fig, axs = plt.subplots(2, figsize=( 10,6), facecolor='#dddddd')
    maxAmplitude=np.unravel_index(SoundfileEngine2.sg_spectrum.argmax(), SoundfileEngine2.sg_spectrum.shape) 
    SoundfileEngine2.subplot_Spectrogram(1,0,1500,SoundfileNominal.Data_Mono_Norm) 
    plt.subplot(2, 1, 2, facecolor='#fff4d6')
    plt.plot(SoundfileEngine2.sg_times, 10*np.log10(SoundfileEngine2.sg_spectrum[maxAmplitude[0],:]), c='r')
    plt.xlim(0,20)
    plt.title("Verlauf der aufbauenden Frequenz in Engine Faulty 2",fontweight='bold',size='medium')
    plt.xlabel('Zeit [s]',size='medium')
    plt.ylabel('Intensität [dB/Hz]',size='medium')
    plt.grid(b=True, which='major', color='black', alpha=0.5, linestyle='dashdot', linewidth=0.5)
    fig.tight_layout()    
    fig.subplots_adjust(top=0.9)
    plt.show()


#   jeden wert mit Samplerate / fft range
def main():

    EngineFaulty1 = Soundfile("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty1.wav", "Engine Faulty 1",'b')
    EngineFaulty2 = Soundfile("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineFaulty2.wav", "Engine Faulty 2",'r')
    EngineNominal = Soundfile("c:/Users/Armin/Source/Repos/NewRepo/Projektaufgabe/engineNominal.wav", "Engine Nominal",'g')

    plot_Spectrogram(Soundfiles=[EngineFaulty1, EngineFaulty2, EngineNominal],StartValue=00, EndValue=2500)
    plot_amplitude_maxfreq(EngineFaulty2)
    #plot spectrogram
    #Diff_EngineFaulty1= EngineFaulty1.Data_Mono_Norm - EngineNominal.Data_Mono_Norm
    #Diff_EngineFaulty2= EngineFaulty2.Data_Mono_Norm - EngineNominal.Data_Mono_Norm
                                                 
    

    #spectrum, frequencies, times= plt.specgram(Diff_EngineFaulty2, NFFT=4096, Fs=EngineFaulty1.SampleRate, noverlap=1024,scale='dB')
    #plt.show()
    #maxAmpl = spectrum.max
    #maxAmpl=np.unravel_index(spectrum.argmax(), spectrum.shape)
    #plt.plot(times, spectrum[41,:])
    #shape=maxfreq.shape()
    #plt.show()




if __name__ == "__main__":
    main()
    #VSC TF
    # use conda install -c conda-forge python-sounddevice