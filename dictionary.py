import csv
import random
import json


class Dictionary:
    written = dict()
    wordlist = list()
    uuid = ""

    def __init__(self, uuid):
        self.load_words()
        self.uuid = uuid

    def load_words(self):
        with open('resources/wordlist') as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            for row in csv_reader:
                if len(row) > 0:
                    if "'" not in row[0] and 3 < len(row[0]) < 10:
                        self.wordlist += row

    def get_next(self):
        return random.choice(self.wordlist)


    def save_written(self, values):
        for key in sorted(values):
            self.written[key] = values[key]

    def save_to_file(self):
        self.save_txt()
        self.saveJson()

    def save_txt(self):
        spaced = ""
        words = []
        for time in sorted(self.written.keys()):
            words += self.written[time]
        contents = "".join(words)
        contents = contents.replace(" ", "*")
        print("Written: " + contents)

        for char in contents:
            spaced += char + "\n"

        with open(r"resources/recordings/" + self.uuid + ".txt", 'w+') as f:
            f.write(spaced)

    def saveJson(self):
        for timestamp in self.written.keys():
            self.written[str(timestamp)] = self.written.pop(timestamp)
        filename = r"resources/recordings/" + self.uuid + ".json"
        with open(filename, 'w+') as f:
            f.write(json.dumps(self.written, ensure_ascii=False))
            print("Saved to: " + filename)
