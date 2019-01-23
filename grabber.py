from Tkinter import *

import sdsrecorder
import utils
from dictionary import Dictionary



# todo text:
#  show progress, pick words based oon missing words,,
#  save map to json?

# todo audio
#  start, pause, resume, finish recording
#  show recording status
#  extract segment for each keypress, then join them in resulting audio and save to file


class Grabber:
    characters_to_write = 0
    dictionary = None
    written = dict()
    uuid = ""
    recorder = None

    def __init__(self, uuid):
        self.uuid = uuid
        self.dictionary = Dictionary(uuid)
        self.recorder = sdsrecorder.Recorder(uuid)
        self.recorder.start_recording()

    def finish_btc_clicked(self):
        print("Finish clicked")
        print("Sending ", self.written)
        self.dictionary.save_written(self.written)
        self.dictionary.save_to_file()
        self.recorder.stop_recording()
        sys.exit(0)

    def start_btc_clicked(self):
        print("Start clicked")

    def pause_btc_clicked(self):
        print("Pause clicked")

    def resume_btc_clicked(self):
        print("Resume clicked")

    def build_ui(self):

        try:
            root = Tk()
            root.geometry('600x400')

            # main frame
            main_frame = Frame(root)
            main_frame.grid()

            # label
            name_label = Label(main_frame, text="Audio & Key Grabber", font=("Arial Bold", 15))
            name_label.grid(column=0, row=0)

            prompt_text = Text(main_frame, bd=2, padx=30, pady=15, font=("Arial Bold", 15), width=40, height=3)
            prompt_text.insert(INSERT, "Text to write will appear here")
            prompt_text.grid(column=0, row=1)

            # user text input
            input_val = StringVar()
            input_val.set('')
            user_text_input = Entry(main_frame, textvariable=input_val, width=40,
                                    font=("Arial Bold", 15))
            user_text_input.grid(column=0, row=2)

            def user_value_changed(a, b, c):
                timestamp = utils.getitimestamp()
                pressed_key = input_val.get()[-1:]
                self.written[timestamp] = pressed_key

                if len(input_val.get()) == self.characters_to_write:
                    self.writing_completed(user_text_input, prompt_text)

            input_val.trace('w', user_value_changed)

            # button frame
            button_frame = Frame(root, pady=15)
            button_frame.grid(column=0, row=3)

            # start button
            start_btn = Button(button_frame, text="Start", command=self.start_btc_clicked)
            start_btn.grid(column=0, row=0)

            # pause button
            pause_btn = Button(button_frame, text="Pause", command=self.pause_btc_clicked)
            pause_btn.grid(column=1, row=0)

            # resume button
            resume_btn = Button(button_frame, text="Resume", command=self.resume_btc_clicked)
            resume_btn.grid(column=2, row=0)

            # finish button
            finish_btn = Button(button_frame, text="Finish", command=self.finish_btc_clicked)
            finish_btn.grid(column=3, row=0)

            # recoding status label
            rec_status_label = Label(button_frame, padx=10, text="Not recording", font=("Arial Bold", 10))
            rec_status_label.grid(column=4, row=0)

            # progress percent value
            progress_value = Label(button_frame, padx=0, text="0", font=("Arial Bold", 10))
            progress_value.grid(column=5, row=0)

            # progress label
            progress_label = Label(button_frame, padx=0, text="% completed", font=("Arial Bold", 10))
            progress_label.grid(column=6, row=0)

            self.show_words(prompt_text)
            root.mainloop()
        except Exception:
            raise Exception("Fuck OOP")

    def append_text(self, text_widget, value):
        self.characters_to_write += len(value)
        text_widget.insert(INSERT, value + " ")

    def clear_text(self, text_widget):
        if text_widget.widgetName == "text":
            text_widget.delete(1.0, END)
        else:
            text_widget.delete(0, END)

    def get_text(self, text_widget):
        return text_widget.get(1.0, END)

    def show_words(self, prompt_text):
        self.characters_to_write = 0
        self.clear_text(prompt_text)
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.characters_to_write += 2  # spaces between words

    def writing_completed(self, user_input, prompter):
        self.clear_text(user_input)
        self.clear_text(prompter)
        self.show_words(prompter)

