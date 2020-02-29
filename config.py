import sounddevice as sd

stroke_time = 0.1
alphabet = "abcdefghijklmnopqrstuvwxyz"
min_strokes_per_key = 15
device_info = sd.query_devices(None, 'input')
samplerate = int(device_info['default_samplerate'])
directory = '/home/tomas/PycharmProjects/grabber/resources/a485-sync/'
subtype = "PCM_32"
device = "default"
channels = 1
