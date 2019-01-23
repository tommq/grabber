import Queue as queue
import sounddevice as sd
import soundfile as sf
import sys
import utils
import threading
import numpy
assert numpy


class Recorder:
    thread = None
    uuid = ""
    go = True

    def __init__(self, uuid):
        self.uuid = uuid

    def record(self):
        try:

            filename = "resources/recordings/" + self.uuid + '.wav'
            device_info = sd.query_devices("default", 'input')
            samplerate = int(device_info['default_samplerate'])
            subtype = "PCM_24"
            device = "default"
            channels = 1
            q = queue.Queue()

            def callback(indata, frames, time, status):
                """This is called (from a separate thread) for each audio block."""
                if status:
                    print(status)
                q.put(indata.copy())

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                              channels=channels, subtype=subtype) as file:
                with sd.InputStream(samplerate=samplerate, device=device,
                                    channels=channels, callback=callback):

                    print('#' * 80)
                    print('press Ctrl+C to stop the recording')
                    print('#' * 80)

                    begin_timestamp = utils.getitimestamp()
                    while self.go is True:
                        file.write(q.get())
                    end_timestamp = utils.getitimestamp()
                    file.__setattr__("comment", str(begin_timestamp) + '&' + str(end_timestamp))

        except KeyboardInterrupt:
            print('\nRecording finished: ')
            sys.exit()
        except Exception as e:
            sys.exit()

    def start_recording(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def stop_recording(self):
        self.go = False
