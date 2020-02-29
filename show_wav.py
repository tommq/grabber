import json
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.io.wavfile import read
import config
import matplotlib.patches as mpatches

def dt_from_str(string_input):
    return dt.strptime(string_input, '%Y-%m-%d %H:%M:%S.%f')

path = config.directory
filename = '47fb06e7'
samplerate, input_data = read(path + filename + ".wav")
print("new has: " + str(len(input_data)))

with open(path + filename + ".json", 'r') as f:
    key_presses = json.load(f)

# search = 5099000
since = 750000
until = 790000
input_data = input_data[since:until]
left, right = input_data[0::2], input_data[1::2]
lf, rf = abs(np.fft.rfft(left)), abs(np.fft.rfft(right))

start = sorted(key_presses)[0]
timestamps = sorted(key_presses)[1:]

plt.figure(figsize=(16, 9))
# a = plt.subplot(211)

for timestamp in sorted(timestamps):
    x = (float(timestamp) - float(start)) * samplerate
    if(x > since and x < until):
        x = x - since
        print(x)
        plt.axvline(x=x - (0.03*44100), c='g')
        plt.axvline(x=x, c='r')
        plt.axvline(x=x + (0.12*44100), c='b')

def toSeconds(x, pos):
    return int(x/44100*1000)


plt.xlabel('time [ms]')
plt.ylabel('Amplitude')
plt.locator_params(nbins=10, axis='y')
plt.locator_params(nbins=40, axis='x')
# plt.minorticks_on()
plt.legend()
plot = plt.plot(input_data)[0]
plot.axes.xaxis.set_major_formatter(FuncFormatter(toSeconds))

red_patch = mpatches.Patch(color='red', label='Recorded time of keypress')
green_patch = mpatches.Patch(color='green', label='Start of audio extraction')
blue_patch = mpatches.Patch(color='blue', label='End of audio extraction')
plt.legend(handles=[red_patch, green_patch, blue_patch])

# c = plt.subplot(212)
# Pxx, freqs, bins, im = c.specgram(input_data, NFFT=1024, Fs=44100, noverlap=900)
# c.set_xlabel('Time')
# c.set_ylabel('Frequency')
plt.show()

