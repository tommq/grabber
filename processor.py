import json
import soundfile as sf

import utils


class Processor:

    uuid = ""
    key_presses = dict()
    recording = None
    samplerate = 0
    press_width = 0
    start_time = None
    end_time = None

    def __init__(self, uuid, width=500):
        self.uuid = uuid
        self.press_width = width

    def get_audio(self):
        self.parse_info(sf.info("resources/recordings/" + self.uuid + ".wav", True))
        self.recording, self.samplerate = sf.read("resources/recordings/" + self.uuid + ".wav")

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
            t1, t2 = str(info.extra_info).split("\n")[14][10:].lstrip().split('&')
            self.start_time = utils.dt_from_str(t1)
            self.end_time = utils.dt_from_str(t2)
        except Exception as e:
            print("Failed to parse start and finish meta information from wav file", e)

    def extract_key_presses(self):
        self.get_audio()
        self.get_json()
        print("File length " + str(len(self.recording) / 44100.0) + " seconds")
        print("Total of " + str(len(self.key_presses)) + " key presses")


