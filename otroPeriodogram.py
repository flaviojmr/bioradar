from pylab import fft, arange, ceil, log10
from pylab import plot, subplot, xlabel, ylabel
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import hilbert

carpeta = "../audioFiles/"
nombre = 'Sentado_30cm_interfaz_1'
ext = '.wav'
arch = carpeta + nombre + ext

fs, data = wavfile.read(arch)

print('> Archivo leído')

data = data/(2.**15)
leng = len(data)
channel1 = data[:,0]

print('> Canales spliteados')

time = arange(0, leng, 1)
channel1 = channel1[0:leng:1]
channelOrig = channel1
print('> Arreglo de tiempo y canal creados')

time = time/fs

plot(time, channel1)
ylabel('Amplitude')
xlabel('Time (s)')
plt.show()


'''
#Generación de señal senoidal

freq = 75.0
time1 = np.arange(leng) / fs
generatedSignal = 2*np.sin(2*np.pi*freq*time1)

print('> Señal arbitraria de ' + str(freq) + ' creada')

#plt.plot(time1, generatedSignal)
#plt.show()
'''


def convert_hertz(freq):
    return freq * 2.0 / 44100.0

def hacerfft(channel1):
    fdata = fft(channel1)

    print('> FFT realizada')
        
    nUniquePts = int(ceil((leng)/2))
    fdata = fdata[0:nUniquePts]
    fdata = abs(fdata)

    fdata = fdata/float(leng)
    fdata = fdata**2

    if leng % 2 > 0:
        fdata[1:int(ceil(len(fdata)))] = fdata[1:int(ceil(len(fdata)))] * 2
    else:
        fdata[1:int(ceil(len(fdata)))-1] = fdata[1:int(ceil(len(fdata)))-1] * 2

    freqArray = arange(0, nUniquePts, 1.0)*(fs/leng)
    plot(freqArray/1000, 10*log10(fdata[0:leng:1]))

    xlabel('Frequency (kHz)')
    ylabel('Power (dB)')
    plt.show()

    print('> FFT graficada')

    return fdata

#hacerfft(channel1)

'''
#Diodo
channel1[channel1 < 0] = 0

plot(time, channel1)
ylabel('Amplitude')
xlabel('Time (s)')

plt.show()

print("> Diodo aplicado")
'''


'''
#Prueba detector de envolvente
channel1 = hilbert(channel1)
channel1 = np.abs(channel1)

plot(time, channel1)
#plot(time, amplitude_envelope)
ylabel('Amplitude')
xlabel('Time (s)')

plt.show()

print("> Envolvente detectada")
'''


#primer filtro pasabajos, diseño y aplicación
gpass = 3
gstop = 10

ord, wn = signal.buttord(convert_hertz(25), convert_hertz(45), gpass, gstop)
b, a = signal.butter(ord, wn, btype='lowpass')

channel1 = signal.lfilter(b, a, channel1)

print('> Primer filtro aplicado')

hacerfft(channel1)

ord, wn = signal.buttord(convert_hertz(25), convert_hertz(30), 2, 7)
b, a = signal.butter(ord, wn, btype='lowpass')

channel1 = signal.lfilter(b, a, channel1)

print('> Segundo filtro aplicado')

hacerfft(channel1)


#Pasabanda

ord, wn = signal.buttord([convert_hertz(26.5), convert_hertz(23.5)], [convert_hertz(21), convert_hertz(29)], gpass, gstop)
b, a = signal.butter(ord, wn, btype='bandpass')
channel1 = signal.lfilter(b, a, channel1)

print('El orden del filtro pasabanda es: ' + str(ord))

hacerfft(channel1)

'''
#mezclado con generatedSignal (mixer)
channel1 = multiply(channel1, generatedSignal)

#hacerfft(channel1)

print('> Señal ya mezclada')
'''

'''
#segundo filtro pasabajos, diseño y aplicación
ord, wn = signal.buttord(convert_hertz(750), convert_hertz(1000), gpass, 30)
b, a = signal.butter(ord, wn, btype='lowpass')

channel1 = signal.lfilter(b, a, channel1)

print('> Segundo filtro aplicado')

#hacerfft(channel1)

#tercer filtro pasabajos, diseño y aplicación
ord, wn = signal.buttord(convert_hertz(300), convert_hertz(450), gpass, 13)
b, a = signal.butter(ord, wn, btype='lowpass')

channel1 = signal.lfilter(b, a, channel1)

print('> Tercer filtro aplicado')

#hacerfft(channel1)

#cuarto filtro pasabajos, diseño y aplicación
ord, wn = signal.buttord(convert_hertz(175), convert_hertz(200), gpass, 8)
b, a = signal.butter(ord, wn, btype='lowpass')

channel1 = signal.lfilter(b, a, channel1)

print('> Cuarto filtro aplicado')
'''

#hacerfft(channel1)

#channel1 = channel1 - mean(channel1)

#print('> "DC removed"')

time = time/fs

plot(time, channel1)
ylabel('Amplitude')
xlabel('Time (s)')

plt.show()

print('> Señal en tiempo graficada')




# Gráfica resumen
subplot(2,1,1)
plot(time, channelOrig)
ylabel('Amplitude')
xlabel('Time (s)  ' + "|  Processed Signal")

subplot(2,1,2)
plot(time, channel1)
ylabel('Amplitude')
xlabel('Time (s)  ' + "|  No Processed Signal")

plt.show()




#print('El valor máximo es: ' + str(10*log10(max(fdata))))

#print('El punto del valor máximo es: ' + str(argmax(fdata)))