import re
import sys
import os
import unicodedata
from collections import Counter
from enum import Enum

# Перевіримо, що ми включили всі необхідні класи
from src.Mode import Mode  # Створений клас Mode
from src.MainWindow import MainWindow  # Включає клас MainWindow для інтерфейсу


# Класи Level та Target для рівнів і цілей
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


# Налаштування для розпізнавання кінця речення
punctuation = '.!?。？！؟ | . !'
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
    return res


def add_and_check_new(val_set, x):
    l = len(val_set)
    val_set.add(x)
    return len(val_set) > l


def bin(text, mode: Mode):
    text = re.sub(r'\s+', ' ', text)  # Замінює всі види пробілів одним пробілом
    n = mode.getN() or 1  # Використовуємо `getN` з Mode

    if mode.lastNode.getLevel() == Level.CHAR.name:
        char_ngrams = ngrams(text, n, "")
        char_set = set()
        char_counter = Counter(char_ngrams)

        if mode.lastNode.getTarget() == Target.EQUAL.name:
            return binare(char_ngrams, lambda x: x == mode.phrase)
        elif mode.lastNode.getTarget() == Target.FREQUENCY.name:
            return binare(char_ngrams, lambda x: mode.getFrequencyFrom() <= char_counter.get(x,
                                                                                             0) <= mode.getFrequencyTo() and not any(
                ch in mode.getStopSymbols() for ch in x))
        elif mode.lastNode.getTarget() == Target.FIRST.name:
            return binare(char_ngrams, lambda x: 1 if add_and_check_new(char_set, x) else 0)

    elif mode.lastNode.getLevel() == Level.WORD.name:
        clean_words = re.sub(r"[^\w" + re.escape(punctuation) + r"]+", " ", text).split()
        word_grams = ngrams(clean_words, n, " ")
        word_set = set()
        word_counter = Counter(word_grams)

        if mode.lastNode.getTarget() == Target.FREQUENCY.name:
            return binare(word_grams, lambda x: mode.getFrequencyFrom() <= word_counter.get(x,
                                                                                            0) <= mode.getFrequencyTo() and not any(
                ch in mode.getStopSymbols() for ch in x))
        elif mode.lastNode.getTarget() == Target.LENGTH.name:
            return binare(word_grams, lambda x: len(x.replace(" ", "")) == mode.getL())

    elif mode.lastNode.getLevel() == Level.SENTENCE.name:
        sentences = sentence_endings.split(text)

        if mode.lastNode.getTarget() == Target.CONTAINS.name:
            return binare(sentences, lambda x: mode.phrase in x)
        elif mode.lastNode.getTarget() == Target.LENGTH.name:
            return binare(sentences, lambda x: len(x.split()) == mode.getL())


def main():
    # Встановлення параметрів через інтерфейс класу Mode
    mode = Mode()
    mode.phrase = 'текст для обробки'  # Вкажіть фразу для обробки

    # Зчитуємо шлях до тексту, якщо вказаний
    params = {'path': '', 'mode': 'print'}
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-i':
            params['path'] = sys.argv[i + 1]

    # Завантаження тексту
    with open(os.path.normpath(params['path']), "r", encoding='utf-8') as file:
        text = file.read().lower()

    # Виконуємо обробку тексту відповідно до режиму
    if params['mode'] == 'print':
        result = bin(text, mode)
        with open("output.csv", "w+", encoding='utf-8') as f:
            f.write(str(result)[1:-1])


if __name__ == '__main__':
    main()
