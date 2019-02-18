import sounddevice as sd

device_info = sd.query_devices("default", 'input')
samplerate = int(device_info['default_samplerate'])
subtype = "PCM_24"
device = "default"
channels = 1
