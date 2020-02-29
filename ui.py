import tkinter as tk
import recorder
from dictionary import Dictionary
from datetime import datetime as dt


class UI:
    characters_to_write = 0
    dictionary = None
    written = dict()
    uuid = ""
    recorder = None
    ui_root = None
    start = None

    def __init__(self, uuid):
        self.uuid = uuid
        self.dictionary = Dictionary(uuid)
        self.recorder = recorder.Recorder(uuid)
        self.recorder.start_recording()
        self.start = dt.now()
        print("UI start" + str(self.start))
        self.ui_root = tk.Tk()

    def finish_btc_clicked(self):
        print("Finish clicked")
        self.dictionary.save_written(self.written)
        self.recorder.stop_recording(self.dictionary)
        self.ui_root.destroy()

    def build_ui(self):

        try:
            self.ui_root.geometry('600x400')

            # main frame
            main_frame = tk.Frame(self.ui_root)
            main_frame.grid()

            # label
            name_label = tk.Label(main_frame, text="Audio & Key Grabber", font=("Arial Bold", 15))
            name_label.grid(column=0, row=0)

            prompt_text = tk.Text(main_frame, bd=2, padx=30, pady=15, font=("Arial Bold", 15), width=40, height=3)
            prompt_text.insert(tk.INSERT, "Text to write will appear here")
            prompt_text.grid(column=0, row=1)

            # user text input
            input_val = tk.StringVar()
            input_val.set('')
            user_text_input = tk.Entry(main_frame, textvariable=input_val, width=40,
                                       font=("Arial Bold", 15))
            user_text_input.grid(column=0, row=2)
            user_text_input.focus()

            def user_value_changed(a, b, c):
                timestamp = self.recorder.streamOuter.time
                pressed_key = input_val.get()[-1:]
                self.written[timestamp] = pressed_key
                self.dictionary.update_letter_counts(pressed_key)
                # print("Keypress at: " + str(self.recorder.streamOuter.time))

                if len(input_val.get()) == self.characters_to_write:
                    self.writing_completed(user_text_input, prompt_text)
                    self.update_progress(progress_value)

            input_val.trace('w', user_value_changed)

            # button frame
            button_frame = tk.Frame(self.ui_root, pady=15)
            button_frame.grid(column=0, row=3)

            # # start button
            # start_btn = Button(button_frame, text="Start", command=self.start_btc_clicked)
            # start_btn.grid(column=0, row=0)
            #
            # # pause button
            # pause_btn = Button(button_frame, text="Pause", command=self.pause_btc_clicked)
            # pause_btn.grid(column=1, row=0)
            #
            # # resume button
            # resume_btn = Button(button_frame, text="Resume", command=self.resume_btc_clicked)
            # resume_btn.grid(column=2, row=0)

            # recoding status label
            rec_status_label = tk.Label(button_frame, padx=10, text="", font=("Arial Bold", 10))
            rec_status_label.grid(column=2, row=0)

            # progress percent value
            progress_value = tk.Label(button_frame, padx=0, text="0", font=("Arial Bold", 10))
            progress_value.grid(column=3, row=0)

            # progress label
            progress_label = tk.Label(button_frame, padx=0, text="% completed   ", font=("Arial Bold", 10))
            progress_label.grid(column=4, row=0)

            # finish button
            finish_btn = tk.Button(button_frame, text="Finish", command=self.finish_btc_clicked)
            finish_btn.grid(column=7, row=0)

            self.show_words(prompt_text)
            self.ui_root.mainloop()
        except Exception as ex:
            raise Exception(ex)

    def append_text(self, text_widget, value):
        self.characters_to_write += len(value)
        text_widget.insert(tk.INSERT, value + " ")

    def clear_text(self, text_widget):
        if text_widget.widgetName == "text":
            text_widget.delete(1.0, tk.END)
        else:
            text_widget.delete(0, tk.END)

    def get_text(self, text_widget):
        return text_widget.get(1.0, tk.END)

    def update_progress(self, progress_value):
        progress_value['text'] = self.dictionary.get_completion_progress()

    def show_words(self, prompt_text):
        self.characters_to_write = 0
        self.clear_text(prompt_text)
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.append_text(prompt_text, self.dictionary.get_next())
        self.characters_to_write += 5  # spaces between words

    def update_words(self, prompt_text, user_input):
        self.characters_to_write = 0
        old = self.get_text(prompt_text).replace("\n", "")
        # print("old: " + old)
        new_word = self.dictionary.get_next() + " "
        remaining_text = ' '.join(old.split(' ')[1:])
        new = remaining_text + new_word
        # print("new: " + new)

        remaining_words = len(new_word) + len(remaining_text)

        self.clear_text(prompt_text)
        self.clear_text(user_input)

        user_input.insert(tk.INSERT, remaining_text)
        self.characters_to_write = remaining_words
        prompt_text.insert(tk.INSERT, new)
        # self.append_text(prompt_text, new)

    def writing_completed(self, user_input, prompter):
        self.update_words(prompter, user_input)
