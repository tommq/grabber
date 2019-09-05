import queue
import sounddevice as sd
import soundfile as sf
import utils
import threading
import numpy
import config

assert numpy


class Recorder:
    thread = None
    uuid = ""
    go = True
    dictionary = None

    def __init__(self, uuid):
        self.uuid = uuid

    def record(self):
        try:
            q = queue.Queue()

            def callback(indata, frames, time, status):
                """This is called (from a separate thread) for each audio block."""
                if status:
                    print(status)
                q.put(indata.copy())

            filename = "resources/recordings/" + self.uuid + '.wav'

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(filename, mode='x', samplerate=config.samplerate,
                              channels=config.channels, subtype=config.subtype) as audio_file:
                with sd.InputStream(samplerate=config.samplerate, device=config.device,
                                    channels=config.channels, callback=callback):
                    print('#' * 80)
                    print('recording')
                    print('#' * 80)

                    begin_timestamp = utils.get_timestamp()
                    while self.go is True:
                        audio_file.write(q.get())
                    print("Recording stopped")
                    # end_timestamp = utils.get_timestamp()
                    self.save_start(begin_timestamp)
                    # audio_file.__setattr__("comment", str(begin_timestamp) + '&' + str(end_timestamp))
                    audio_file.close()
                    print("Finished writing file")

        except Exception as e:
            print("Ex in recording " + str(e))

    def start_recording(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def save_start(self, start):
        self.dictionary.save_to_file(start)

    def stop_recording(self, dictionary):
        self.dictionary = dictionary
        self.go = False
