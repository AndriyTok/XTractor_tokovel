import os
import sys
import re
from collections import Counter
from enum import Enum

from src.Chooser import Chooser
from src.CsvBuilder import CsvBuilder
from src.IOUtils import IOUtils
from src.MainWindow import Node, ValueType, MainWindow
from src.Mode import Mode


class Level(Enum):
    CHAR = 0
    LETTER = 1
    WORD = 2
    SENTENCE = 3


class Target(Enum):
    LENGTH = 0
    FREQUENCY = 1
    EQUAL = 2
    STARTS = 3
    CONTAINS = 4
    ENDS = 5
    FIRST = 6


# Punctuation and regex for sentence endings
punctuation = '.!?。？！؟'
sentence_endings = re.compile(r"(?<!\w\.\w.)(?<![А-Я][а-я]\.)(?<![А-Я]\.)(?<=\.|\?|\!|。|？|！|؟)\s+")


def ngrams(arr, n, join_divider):
    if not join_divider:
        return [arr[i:i + n] for i in range(len(arr) - n + 1)]
    else:
        return [join_divider.join(arr[i:i + n]) for i in range(len(arr) - n + 1)]


def binare(arr, expression):
    res = [0] * len(arr)
    for i, x in enumerate(arr):
        res[i] = (1, x) if expression(x) else (0, x)
        if i % 1000 == 0:
            print(f'{100 * (i / len(arr)):.2f}%')
    return res


def add_and_check_new(val_set, x):
    l = len(val_set)
    val_set.add(x)
    return len(val_set) > l


def bin(text, level, target, sublevel=None, s='', ff=1, ft=1, ss=[], n=1, l=1):
    text = re.sub(r'\s+', ' ', text)  # Replace all types of spaces with a single space

    if level == Level.CHAR.name or level == Level.LETTER.name:
        n = n if n > 0 else len(s) if s else 1
        char_ngrams = ngrams(text, n, "")
        char_set = set()
        char_counter = Counter(char_ngrams)

        if target == Target.EQUAL.name:
            return binare(char_ngrams, lambda x: x == s)
        elif target == Target.FREQUENCY.name:
            return binare(char_ngrams, lambda x: ff <= char_counter.get(x, 0) <= ft and not any(ch in ss for ch in x))
        elif target == Target.FIRST.name:
            return binare(char_ngrams, lambda x: 1 if add_and_check_new(char_set, x) else 0)

    elif level == Level.WORD.name:
        n = n if n > 0 else len(str(s).split()) if s else 1
        clean_words = re.sub(r"[^\w" + re.escape(punctuation) + r"]+", " ", text).split()
        word_grams = ngrams(clean_words, n, " ")
        word_set = set()
        word_counter = Counter(word_grams)

        if target == Target.EQUAL.name:
            return binare(word_grams, lambda x: s == x)
        elif target == Target.FREQUENCY.name:
            return binare(word_grams, lambda x: ff <= word_counter.get(x, 0) <= ft and not any(ch in ss for ch in x))
        elif target == Target.LENGTH.name:
            return binare(word_grams, lambda x: len(re.sub(r"[^\w" + re.escape(punctuation) + r"]", "", x)) == l)
        elif target == Target.STARTS.name:
            return binare(word_grams, lambda x: x.startswith(s))
        elif target == Target.CONTAINS.name:
            return binare(word_grams, lambda x: s in x)
        elif target == Target.ENDS.name:
            return binare(word_grams, lambda x: x.endswith(s))
        elif target == Target.FIRST.name:
            return binare(word_grams, lambda x: 1 if add_and_check_new(word_set, x) else 0)

    elif level == Level.SENTENCE.name:
        sentences = sentence_endings.split(text)
        if target == Target.CONTAINS.name:
            return binare(sentences, lambda x: s in x)
        elif target == Target.LENGTH.name:
            return binare(sentences, lambda x: len(re.sub(r"[^\w" + re.escape(punctuation) + r"]", "", x)) == l)


def print_all(text, level, target, sublevel=None, s='', ff=1, ft=1, ss=[], n=1, l=0):
    text = re.sub(r'\s+', ' ', text)
    n = max(n, 1)
    if level == Level.CHAR.name:
        char_counter = Counter(text)
        return [char_counter.get(ch, 0) for ch in text]
    elif level == Level.WORD.name:
        clean_words = re.sub(r"[^\w" + re.escape(punctuation) + r"]+", " ", text).split()
        word_grams = ngrams(clean_words, n, " ")
        word_counter = Counter(word_grams)
        return [len(word) for word in word_grams]


def bin_to_dt(bin_arr):
    ix = [i for i, x in enumerate(bin_arr) if x == 1]
    return [ix[i + 1] - ix[i] for i in range(len(ix) - 1)]


def main():
    chooser = Chooser()  # Create an instance of Chooser
    root = chooser.get_root()  # Get the Tk root window

    # Get the file path to open
    params = {
        'path': chooser.get_file_path(),
        'level': '',
        'target': '',
        'sublevel': None,
        'symbol': '',
        'freq_from': 1,
        'freq_to': 1,
        'stop_symbols': [],
        'n': 1,
        'l': 1,
        'mode': 'print'
    }

    if not params['path']:  # Check if the user canceled the file selection
        print("No file selected.")
        return

    # Use IOUtils to read the file
    text = IOUtils.read_file(os.path.normpath(params['path'])).lower()

    # Instantiate MainWindow with the Tk root
    main_window = MainWindow(root)  # Pass the root to MainWindow

    if params['mode'] == 'print':
        res = print_all(text, params['level'], params['target'], params['sublevel'], params['symbol'], params['freq_from'], params['freq_to'], params['stop_symbols'], params['n'], params['l'])

        if res is None:  # Check if res is None before proceeding
            print("No results returned.")
            return

        # Use CsvBuilder to write the CSV
        csv_builder = CsvBuilder(',')  # Initialize with default comma delimiter
        for item in res:
            csv_builder.add(item).new_line()  # Add items and create new lines
        output_path = chooser.get_file_to_save_csv()  # Get file path for CSV
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(csv_builder))  # Write to CSV file

        main_window.display_results(res)  # Display results in the GUI

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == '__main__':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    main()
