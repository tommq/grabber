import sounddevice as sd


stroke_time = 0.1
alphabet = "abcdefghijklmnopqrstuvwxyz"
min_strokes_per_key = 5
device_info = sd.query_devices("default", 'input')
samplerate = int(device_info['default_samplerate'])
subtype = "DOUBLE"
device = "default"
channels = 1
