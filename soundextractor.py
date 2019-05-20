import queue
import json

import sounddevice as sd
import soundfile as sf

import config
import utils


class SoundExtractor:

    uuid = ""
    key_presses = dict()
    recording = None
    samplerate = 0
    start_time = None
    end_time = None
    stroke_time = None
    input_audiofile = None

    def __init__(self, uuid):
        self.uuid = uuid
        self.input_audiofile = "resources/recordings/" + self.uuid + "_raw.wav"
        self.stroke_time = config.stroke_time
        print("#################  EXTRACTOR #################")

    def get_audio(self):
        self.parse_info(sf.info(self.input_audiofile, True))
        self.recording, self.samplerate = sf.read(self.input_audiofile)

    def get_json(self):
        try:
            with open("resources/recordings/" + self.uuid + ".json") as f:
                unicode_dict = json.load(f)
                for key in unicode_dict.keys():
                    self.key_presses[utils.dt_from_str(str(key))] = str(unicode_dict[key])
        except Exception as e:
            print(self.key_presses, e)

    def parse_info(self, info):
        try:
            # print(info.extra_info)
            for line in str(info.extra_info).split("\n"):
                line = line.lstrip()
                if line.startswith("ICMT"):
                    t1,t2 = line.lstrip()[7:].split('&')
                    self.start_time = utils.dt_from_str(t1)
                    self.end_time = utils.dt_from_str(t2)
                    return

            print("Failed to parse meta")
        except Exception as e:
            print("Failed to parse start and finish meta information from wav file", e)
            print(str(info.extra_info))

    def extract_key_presses(self):
        self.load_files()
        self.create_output_file()

    def create_output_file(self):

        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status)
            q.put(indata.copy())

        try:
            with sf.SoundFile("resources/recordings/" + self.uuid + ".wav", mode='x', samplerate=config.samplerate,
                              channels=config.channels, subtype=config.subtype) as output_file:
                with sd.InputStream(samplerate=self.samplerate, device=config.device,
                                    channels=config.channels, callback=callback):
                    print("Found original file with length " + str(len(self.recording) / self.samplerate) + " s")
                    print("Start of recording " + str(self.start_time))
                    data_size = len(self.recording)
                    print("Data size: " + str(data_size) + " shape: " + str(self.recording.shape))
                    input_file = sf.SoundFile(self.input_audiofile)
                    for keypress in sorted(self.key_presses.keys()):
                        relative_time = keypress - self.start_time
                        start_block = int((relative_time.total_seconds() - self.stroke_time) * self.samplerate)
                        end_block = int((relative_time.total_seconds() + self.stroke_time) * self.samplerate)

                        print(self.key_presses[keypress] + " at " + str(relative_time) + " -> extracting range " + str(start_block) + " to " + str(end_block))
                        block_range = end_block-start_block
                        # print("range: " + str(block_range))
                        input_file.seek(start_block)
                        audio_buffer = input_file.buffer_read(frames=block_range, dtype='float64')
                        # print(len(audio_buffer))
                        output_file.buffer_write(audio_buffer, dtype='float64')

                    print("End of recording " + str(self.end_time))
                    input_file.close()

            self.exit_prog()
        except Exception as ex:
            print("Dang it" + str(ex))

    def load_files(self):
        self.get_audio()
        self.get_json()
        print("File length " + str(len(self.recording) / 44100.0) + " seconds")
        print("Total of " + str(len(self.key_presses)) + " key presses")

    def exit_prog(self):
        pass
        # sys.exit(0)