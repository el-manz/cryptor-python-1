import math
import random
from tkinter import *
from dataclasses import dataclass

alphabet = [x.to_bytes(1, byteorder='big', signed=True).decode() for x in range(128)]

positions = dict()
for pos in range(len(alphabet)):
    positions[alphabet[pos]] = pos


def check_text(text):
    for symbol in text:
        if symbol not in alphabet:
            return False
    return True


def caesar_encryption(text_to_decrypt, shift):
    def decrypt_letter(symbol_to_decrypt):
        return alphabet[(positions[symbol_to_decrypt] + shift) % len(alphabet)]

    answer = """"""
    for symbol in text_to_decrypt:
        answer += decrypt_letter(symbol)

    return answer


def caesar_decryption(text_to_encrypt, shift):
    return caesar_encryption(text_to_encrypt, -shift)


def vigenere_encryption(text_to_decrypt, keyword):
    def decrypt_letter(symbol_to_decrypt, index):
        shift = positions[keyword[index % len(keyword)]]
        return alphabet[(positions[symbol_to_decrypt] + shift) % len(alphabet)]

    answer = """"""
    for i in range(len(text_to_decrypt)):
        answer += decrypt_letter(text_to_decrypt[i], i)
    return answer


def vigenere_decryption(text_to_decrypt, keyword):
    def decrypt_letter(symbol_to_decrypt, index):
        shift = positions[keyword[index % len(keyword)]]
        return alphabet[(positions[symbol_to_decrypt] - shift) % len(alphabet)]

    answer = """"""
    for i in range(len(text_to_decrypt)):
        answer += decrypt_letter(text_to_decrypt[i], i)
    return answer


def vernam_encryption(text_to_decrypt):
    def generate_sequence():
        base = math.ceil(math.log(len(alphabet)))

        def generate_chunk():
            temp_chunk = 0
            coefficient = 1
            for j in range(base):
                temp_chunk += random.randint(0, 1) * coefficient
                coefficient *= 2
            return temp_chunk

        generate_keys = []
        for k in range(len(text_to_decrypt)):
            generate_keys.append(generate_chunk())
        return generate_keys

    keys = generate_sequence()

    def decrypt_letter(symbol_to_decrypt, get_keys, index):
        return alphabet[(positions[symbol_to_decrypt] ^ get_keys[index]) % len(alphabet)]

    answer = """"""
    for i in range(len(text_to_decrypt)):
        answer += decrypt_letter(text_to_decrypt[i], keys, i)
    return [answer, keys]


def vernam_decryption(text_to_decrypt, keys):
    def decrypt_letter(symbol_to_decrypt, get_keys, index):
        return alphabet[(positions[symbol_to_decrypt] ^ get_keys[index]) % len(alphabet)]

    answer = """"""
    for i in range(len(text_to_decrypt)):
        answer += decrypt_letter(text_to_decrypt[i], keys, i)
    return answer


@dataclass(order=True)
class LetterFrequency:
    frequency: int
    letter: str

    def __init__(self, _letter, _text):
        self.letter = _letter.upper()
        self.frequency = _text.count(self.letter)


def build_frequencies(text):
    text = text.upper()

    frequencies = []
    sum = 0
    for i in range(len(alphabet)):
        frequencies.append(LetterFrequency(alphabet[i], text))
        sum += frequencies[i].frequency
    for i in range(len(frequencies)):
        frequencies[i].frequency = frequencies[i].frequency / sum
    frequencies.sort()
    return frequencies


def frequency_analysis(text_to_decrypt, standard_text):
    standard_frequencies = build_frequencies(standard_text)

    to_decrypt_frequencies = build_frequencies(text_to_decrypt)

    to_decrypt_most_common = positions[to_decrypt_frequencies[-1].letter]
    language_most_common = positions[standard_frequencies[-1].letter]
    shift = abs(to_decrypt_most_common - language_most_common)

    def decrypt_letter(symbol_to_decrypt):
        return alphabet[(positions[symbol_to_decrypt] - shift) % len(alphabet)]

    answer = """"""
    for symbol in text_to_decrypt:
        answer += decrypt_letter(symbol)

    return answer


class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("CryptorPython")
        self.geometry("500x580")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartingWindow, CaesarEncryptionWindow, CaesarDecryptionWindow, VigenereEncryptionWindow,
                  VigenereDecryptionWindow, VernamEncryptionWindow, VernamDecryptionWindow, FrequencyAnalysisWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartingWindow")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartingWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        caesar_encryption_mode = Button(self, text="Caesar Encryption", width=50, height=4,
                                        command=lambda: controller.show_frame("CaesarEncryptionWindow"))
        caesar_encryption_mode.pack(side=TOP, pady=13)
        caesar_decryption_mode = Button(self, text="Caesar Decryption", width=50, height=4,
                                        command=lambda: controller.show_frame("CaesarDecryptionWindow"))
        caesar_decryption_mode.pack(side=TOP, pady=0)
        vigenere_encryption_mode = Button(self, text="Vigenere Encryption", width=50, height=4,
                                          command=lambda: controller.show_frame("VigenereEncryptionWindow"))
        vigenere_encryption_mode.pack(side=TOP, pady=13)
        vigenere_decryption_mode = Button(self, text="Vigenere Decryption", width=50, height=4,
                                          command=lambda: controller.show_frame("VigenereDecryptionWindow"))
        vigenere_decryption_mode.pack(side=TOP, pady=0)
        vernam_encryption_mode = Button(self, text="Vernam Encryption", width=50, height=4,
                                        command=lambda: controller.show_frame("VernamEncryptionWindow"))
        vernam_encryption_mode.pack(side=TOP, pady=13)
        vernam_decryption_mode = Button(self, text="Vernam Decryption", width=50, height=4,
                                        command=lambda: controller.show_frame("VernamDecryptionWindow"))
        vernam_decryption_mode.pack(side=TOP, pady=0)
        frequency_analysis_mode = Button(self, text="Frequency Analysis", width=50, height=4,
                                         command=lambda: controller.show_frame("FrequencyAnalysisWindow"))
        frequency_analysis_mode.pack(side=TOP, pady=13)


class CaesarEncryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def save_key_to_file(key, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(key)
            file_to_save.close()

        def insert_keyword(path_to_file, entry_shift):
            shift = int(entry_shift.get())
            file = open(path_to_file)

            to_encrypt = file.read()

            encrypted = ""
            if not check_text(to_encrypt):
                encrypted = "Text contains wrong symbols!"
            else:
                encrypted = caesar_encryption(to_encrypt, shift)

            entry_path_encrypted = Entry(self, width=15)
            entry_path_encrypted.place(anchor=CENTER, relx=0.17, rely=0.6)
            button_save_encrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(encrypted, entry_path_encrypted))
            button_save_encrypted.place(anchor=E, relx=0.47, rely=0.6)

            entry_path_key = Entry(self, width=15)
            entry_path_key.place(anchor=CENTER, relx=0.67, rely=0.6)
            button_save_key = Button(self, text="Save key",
                                     command=lambda: save_key_to_file(str(shift), entry_path_key))
            button_save_key.place(anchor=E, relx=0.97, rely=0.6)

            text = Text(width=50, height=13)
            text.insert(INSERT, encrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.7, relheight=0.3)
            text.place(anchor=N, relx=0.5, rely=0.7)
            text.config(yscrollcommand=scroll.set)

        def insert_path():
            file_to_encrypt = entry_path.get()
            label_shift = Label(self, text="Enter shift")
            label_shift.config(bd=20)
            label_shift.pack(side=TOP)
            entry_shift = Entry(self, width=50)
            entry_shift.pack(side=TOP)
            button_shift = Button(self, text="Enter", command=lambda: insert_keyword(file_to_encrypt, entry_shift))
            button_shift.pack(side=TOP)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class CaesarDecryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def insert_keyword(path_to_file, entry_shift, entry_path_shift):

            shift = 0

            if len(entry_shift.get()) != 0:
                shift = int(entry_shift.get())

            file = open(path_to_file)

            key_path_to_file = entry_path_shift.get()
            if len(key_path_to_file) != 0:
                key_file = open(key_path_to_file)
                shift = int(key_file.read())

            to_decrypt = file.read()

            decrypted = ""
            if not check_text(to_decrypt):
                decrypted = "Text contains wrong symbols!"
            else:
                decrypted = caesar_decryption(to_decrypt, shift)

            entry_path_decrypted = Entry(self, width=40)
            entry_path_decrypted.place(anchor=CENTER, relx=0.45, rely=0.6)
            button_save_decrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(decrypted, entry_path_decrypted))
            button_save_decrypted.place(anchor=E, relx=0.97, rely=0.6)

            text = Text(width=50, height=13)
            text.insert(INSERT, decrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.7, relheight=0.3)
            text.place(anchor=N, relx=0.5, rely=0.7)
            text.config(yscrollcommand=scroll.set)

        def insert_path():
            file_to_decrypt = entry_path.get()
            label_shift = Label(self, text="    Enter shift...         "
                                           "                                       ...or insert path to key-file")
            label_shift.config(bd=20)
            label_shift.pack(side=TOP)
            entry_shift = Entry(self, width=12)
            entry_shift.pack(side=LEFT, padx=15, anchor=N)
            entry_path_shift = Entry(self, width=10)
            button_shift = Button(self, text="Enter",
                                  command=lambda: insert_keyword(file_to_decrypt, entry_shift, entry_path_shift))
            button_shift.pack(side=LEFT, anchor=N)
            button_path_shift = Button(self, text="Enter",
                                       command=lambda: insert_keyword(file_to_decrypt, entry_shift, entry_path_shift))
            button_path_shift.pack(side=RIGHT, padx=15, anchor=N)
            entry_path_shift.pack(side=RIGHT, anchor=N)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class FrequencyAnalysisWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def insert_path():
            path_to_decrypt = entry_path.get()
            file_to_decrypt = open(path_to_decrypt, 'r')
            to_decrypt = file_to_decrypt.read()

            decrypted = ""
            if not check_text(to_decrypt):
                decrypted = "Text contains wrong symbols!"
            else:
                standard_file = open("standard.txt")
                standard_text = standard_file.read()
                decrypted = frequency_analysis(to_decrypt, standard_text)

            entry_path_decrypted = Entry(self, width=40)
            entry_path_decrypted.place(anchor=CENTER, relx=0.45, rely=0.3)
            button_save_decrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(decrypted, entry_path_decrypted))
            button_save_decrypted.place(anchor=E, relx=0.97, rely=0.3)

            text = Text(width=50, height=40)
            text.insert(INSERT, decrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.4, relheight=0.6)
            text.place(anchor=N, relx=0.5, rely=0.4)
            text.config(yscrollcommand=scroll.set)


        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class VigenereEncryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def save_key_to_file(key, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(key)
            file_to_save.close()

        def insert_keyword(path_to_file, entry_shift):
            keyword = entry_shift.get()
            file = open(path_to_file)

            to_encrypt = file.read()

            encrypted = ""
            if not check_text(to_encrypt):
                encrypted = "Text contains wrong symbols!"
            else:
                encrypted = vigenere_encryption(to_encrypt, keyword)

            entry_path_encrypted = Entry(self, width=15)
            entry_path_encrypted.place(anchor=CENTER, relx=0.17, rely=0.6)
            button_save_encrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(encrypted, entry_path_encrypted))
            button_save_encrypted.place(anchor=E, relx=0.47, rely=0.6)

            entry_path_key = Entry(self, width=15)
            entry_path_key.place(anchor=CENTER, relx=0.67, rely=0.6)
            button_save_key = Button(self, text="Save key",
                                     command=lambda: save_key_to_file(keyword, entry_path_key))
            button_save_key.place(anchor=E, relx=0.97, rely=0.6)

            text = Text(width=50, height=13)
            text.insert(INSERT, encrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.7, relheight=0.3)
            text.place(anchor=N, relx=0.5, rely=0.7)
            text.config(yscrollcommand=scroll.set)

        def insert_path():
            file_to_encrypt = entry_path.get()
            label_shift = Label(self, text="Enter keyword")
            label_shift.config(bd=20)
            label_shift.pack(side=TOP)
            entry_shift = Entry(self, width=50)
            entry_shift.pack(side=TOP)
            button_shift = Button(self, text="Enter", command=lambda: insert_keyword(file_to_encrypt, entry_shift))
            button_shift.pack(side=TOP)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class VigenereDecryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def insert_keyword(path_to_file, entry_shift, entry_path_shift):

            keyword = 0

            if len(entry_shift.get()) != 0:
                keyword = entry_shift.get()

            file = open(path_to_file)

            key_path_to_file = entry_path_shift.get()
            if len(key_path_to_file) != 0:
                key_file = open(key_path_to_file)
                keyword = key_file.read()

            to_decrypt = file.read()

            decrypted = ""
            if not check_text(to_decrypt):
                decrypted = "Text contains wrong symbols!"
            else:
                decrypted = vigenere_decryption(to_decrypt, keyword)

            entry_path_decrypted = Entry(self, width=40)
            entry_path_decrypted.place(anchor=CENTER, relx=0.45, rely=0.6)
            button_save_decrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(decrypted, entry_path_decrypted))
            button_save_decrypted.place(anchor=E, relx=0.97, rely=0.6)

            text = Text(width=50, height=13)
            text.insert(INSERT, decrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.7, relheight=0.3)
            text.place(anchor=N, relx=0.5, rely=0.7)
            text.config(yscrollcommand=scroll.set)

        def insert_path():
            file_to_decrypt = entry_path.get()
            label_shift = Label(self, text="    Enter keyword...         "
                                           "                                       ...or insert path to key-file")
            label_shift.config(bd=20)
            label_shift.pack(side=TOP)
            entry_shift = Entry(self, width=12)
            entry_shift.pack(side=LEFT, padx=15, anchor=N)
            entry_path_shift = Entry(self, width=10)
            button_shift = Button(self, text="Enter",
                                  command=lambda: insert_keyword(file_to_decrypt, entry_shift, entry_path_shift))
            button_shift.pack(side=LEFT, anchor=N)
            button_path_shift = Button(self, text="Enter",
                                       command=lambda: insert_keyword(file_to_decrypt, entry_shift, entry_path_shift))
            button_path_shift.pack(side=RIGHT, padx=15, anchor=N)
            entry_path_shift.pack(side=RIGHT, anchor=N)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class VernamEncryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def save_key_to_file(key, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            for shift in key:
                file_to_save.write(str(shift))
                file_to_save.write("\n")
            file_to_save.close()

        def insert_path():
            file = open(entry_path.get())

            to_encrypt = file.read()

            encrypted = ""
            if not check_text(to_encrypt):
                encrypted = "Text contains wrong symbols!"
            else:
                encrypted = vernam_encryption(to_encrypt)

            entry_path_encrypted = Entry(self, width=15)
            entry_path_encrypted.place(anchor=CENTER, relx=0.17, rely=0.4)
            button_save_encrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(encrypted[0], entry_path_encrypted))
            button_save_encrypted.place(anchor=E, relx=0.47, rely=0.4)

            keyword = encrypted[1]
            entry_path_key = Entry(self, width=15)
            entry_path_key.place(anchor=CENTER, relx=0.67, rely=0.4)
            button_save_key = Button(self, text="Save key",
                                     command=lambda: save_key_to_file(keyword, entry_path_key))
            button_save_key.place(anchor=E, relx=0.97, rely=0.4)

            text = Text(width=50, height=30)
            text.insert(INSERT, encrypted[0])
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.5, relheight=0.5)
            text.place(anchor=N, relx=0.5, rely=0.5)
            text.config(yscrollcommand=scroll.set)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=15)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


class VernamDecryptionWindow(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        def save_to_file(encrypted, entry_path_to_save):
            path_to_save = entry_path_to_save.get()
            file_to_save = open(path_to_save, 'w')
            file_to_save.write(encrypted)
            file_to_save.close()

        def insert_keyword(path_to_file, entry_path_shift):
            file = open(path_to_file)

            key_path_to_file = entry_path_shift.get()
            key_file = open(key_path_to_file)
            keyword = key_file.read()
            keys = keyword.split('\n')

            temp = []
            for i in range(len(keys) - 1):
                temp.append(int(keys[i]))

            keys = temp

            to_decrypt = file.read()

            decrypted = ""
            if not check_text(to_decrypt):
                decrypted = "Text contains wrong symbols!"
            else:
                decrypted = vernam_decryption(to_decrypt, keys)

            entry_path_decrypted = Entry(self, width=40)
            entry_path_decrypted.place(anchor=CENTER, relx=0.45, rely=0.6)
            button_save_decrypted = Button(self, text="Save text",
                                           command=lambda: save_to_file(decrypted, entry_path_decrypted))
            button_save_decrypted.place(anchor=E, relx=0.97, rely=0.6)

            text = Text(width=50, height=13)
            text.insert(INSERT, decrypted)
            text.configure(state='disabled')
            scroll = Scrollbar(command=text.yview)
            scroll.place(relx=0, rely=0.7, relheight=0.3)
            text.place(anchor=N, relx=0.5, rely=0.7)
            text.config(yscrollcommand=scroll.set)

        def insert_path():
            file_to_decrypt = entry_path.get()
            label_shift = Label(self, text="Insert path to key-file")
            label_shift.config(bd=20)
            label_shift.pack(side=TOP)
            entry_path_shift = Entry(self, width=50)
            entry_path_shift.pack(side=TOP)
            button_path_shift = Button(self, text="Enter",
                                       command=lambda: insert_keyword(file_to_decrypt, entry_path_shift))
            button_path_shift.pack(side=TOP)

        label_path = Label(self, text="Enter path to file")
        label_path.config(bd=20)
        label_path.pack(side=TOP, pady=5)
        entry_path = Entry(self, width=50)
        entry_path.pack(side=TOP)
        button_path = Button(self, text="Enter", command=insert_path)
        button_path.pack(side=TOP)


if __name__ == "__main__":
    window = Window()
    window.mainloop()
