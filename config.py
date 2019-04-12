import sounddevice as sd

stroke_time = 0.1
alphabet = "abcdefghijklmnopqrstuvwxyz"
min_strokes_per_key = 30
device_info = sd.query_devices("default", 'input')
samplerate = int(device_info['default_samplerate'])
directory = '/home/tomas/Documents/School/Master-thesis/thesis-resources/a485-kb/recordings/'
subtype = "PCM_32"
device = "default"
channels = 1
