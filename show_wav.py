import wave
from scipy import signal
import json
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def dt_from_str(string_input):
    return dt.strptime(string_input, '%Y-%m-%d %H:%M:%S.%f')

signal_wave = wave.open('/home/tomas/Documents/School/Master-thesis/thesis-resources/a485-kb/recordings/51dc68c6.wav', 'r')
nframes = signal_wave.getnframes()
print("Have frames: " + str(nframes))
sample_frequency = 44100

data = np.frombuffer(signal_wave.readframes(sample_frequency), dtype=np.int32)

key_presses = dict()

with open('/home/tomas/Documents/School/Master-thesis/thesis-resources/a485-kb/recordings/51dc68c6.json', 'r') as f:
    unicode_dict = json.load(f)
    for key in unicode_dict.keys():
        key_presses[dt_from_str(str(key))] = str(unicode_dict[key])

sig = signal_wave.readframes(nframes)
sig = np.frombuffer(sig, dtype=np.int32)
print(len(sig))
sig = sig[:]
left, right = data[0::2], data[1::2]
lf, rf = abs(np.fft.rfft(left)), abs(np.fft.rfft(right))

start = sorted(key_presses)[0]
timestamps = sorted(key_presses)[1:]

plt.figure(1)
a = plt.subplot(211)
for timestamp in sorted(timestamps):
    x = (timestamp-start).total_seconds() * 44100
    print(x)
    a.axvline(x=x, c='r')

a.set_xlabel('time [s]')
a.set_ylabel('sample value [-]')
plt.plot(sig)
c = plt.subplot(212)
Pxx, freqs, bins, im = c.specgram(sig, NFFT=1024, Fs=16000, noverlap=900)
c.set_xlabel('Time')
c.set_ylabel('Frequency')
plt.show()

