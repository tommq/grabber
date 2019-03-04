import csv
import random
import json

import config


class Dictionary:
    written_letters = dict()
    letter_counts = dict()
    wordlist = list()
    uuid = ""
    min_strokes = None
    total = None

    def __init__(self, uuid):
        self.load_words()
        self.uuid = uuid
        self.min_strokes = config.min_strokes_per_key
        self.total = len(config.alphabet) * self.min_strokes
        self.init_dict()

    def init_dict(self):
        for character in config.alphabet:
            self.letter_counts[character] = 0

    def load_words(self):
        with open('resources/wordlist') as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            for row in csv_reader:
                if len(row) > 0:
                    if "'" not in row[0] and 3 < len(row[0]) < 10:
                        self.wordlist += row

    def get_next(self):
        character = min(self.letter_counts, key=self.letter_counts.get)
        return self.get_next_cointaining(character)

    def get_next_cointaining(self, character):
        while True:
            chosen = random.choice(self.wordlist)
            if character in chosen:
                return chosen

    def get_completion_progress(self):
        progress = round(sum(self.letter_counts.values())/float(self.total)*100, 1)
        return progress

    def save_written(self, values):
        for key in sorted(values):
            self.written_letters[key] = values[key]

    def update_letter_counts(self, values):
        for key in values:
            if key in self.letter_counts:
                if self.letter_counts[key] <= self.min_strokes:
                    self.letter_counts[key] = self.letter_counts[key]+1

    def save_to_file(self):
        self.save_txt()
        self.saveJson()

    def save_txt(self):
        spaced = ""
        words = []
        for time in sorted(self.written_letters.keys()):
            words += self.written_letters[time]
        contents = "".join(words)
        contents = contents.replace(" ", "*")
        print("Written: " + contents)

        for char in contents:
            spaced += char + "\n"

        with open(r"resources/recordings/" + self.uuid + ".txt", 'w+') as f:
            f.write(spaced)

    def saveJson(self):
        for timestamp in self.written_letters.keys():
            self.written_letters[str(timestamp)] = self.written_letters.pop(timestamp)
        filename = r"resources/recordings/" + self.uuid + ".json"
        with open(filename, 'w+') as f:
            f.write(json.dumps(self.written_letters, ensure_ascii=False))
            print("Saved to: " + filename)
