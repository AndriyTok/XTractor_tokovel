class Constants:
    WHITESPACE_V0 = "\u0009"
    WHITESPACE_V1 = "\u000B"
    WHITESPACE_V2 = "\u000C"
    WHITESPACE_V3 = "\u0020"
    WHITESPACE_V4 = "\u0085"
    WHITESPACE_V5 = "\u00A0"
    WHITESPACE_V6 = "\u1680"
    WHITESPACE_V7 = "\u180E"
    WHITESPACE_V8 = "\u2000"
    WHITESPACE_V9 = "\u2001"
    WHITESPACE_V10 = "\u2002"
    WHITESPACE_V11 = "\u2003"
    WHITESPACE_V12 = "\u2004"
    WHITESPACE_V13 = "\u2005"
    WHITESPACE_V14 = "\u2006"
    WHITESPACE_V15 = "\u2007"
    WHITESPACE_V16 = "\u2008"
    WHITESPACE_V17 = "\u2009"
    WHITESPACE_V18 = "\u200A"
    WHITESPACE_V19 = "\u2028"
    WHITESPACE_V20 = "\u2029"
    WHITESPACE_V21 = "\u202F"
    WHITESPACE_V22 = "\u205F"
    WHITESPACE_V23 = "\u3000"
    WHITESPACE = r"\s"

    APOSTROPHE_V0 = "\u0027"
    APOSTROPHE_V1 = "\u2019"
    APOSTROPHE_V2 = "\u02BC"
    APOSTROPHE_V3 = "\u02BB"
    APOSTROPHE_V4 = "\u02BB"
    APOSTROPHE_V5 = "\u055A"
    APOSTROPHE_V6 = "\uA78B"
    APOSTROPHE_V7 = "\u0060"
    APOSTROPHE = (
            APOSTROPHE_V0 + APOSTROPHE_V1 + APOSTROPHE_V2 + APOSTROPHE_V3 +
            APOSTROPHE_V4 + APOSTROPHE_V5 + APOSTROPHE_V6 + APOSTROPHE_V7
    )

    DASH_V0 = "\u002D"
    DASH_V2 = "\u00AF"
    DASH_V3 = "\u02C9"
    DASH_V4 = "\u02CD"
    DASH_V5 = "\u02D7"
    DASH_V6 = "\u02DC"
    DASH_V7 = "\u2010"
    DASH_V8 = "\u2011"
    DASH_V9 = "\u203E"
    DASH_V10 = "\u2043"
    DASH_V11 = "\u207B"
    DASH_V12 = "\u208B"
    DASH_V13 = "\u2212"
    DASH_V14 = "\u23AF"
    DASH_V15 = "\u23E4"
    DASH_V16 = "\u2500"
    DASH_V17 = "\u2796"
    DASH = r"\-"

    UA_SYMBOLS_ONLY = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'\\-"
    UA_SYMBOLS = UA_SYMBOLS_ONLY + UA_SYMBOLS_ONLY.upper()

    RU_SYMBOLS_ONLY = "абвгдеёэжзыийклмнопрстуфхцчшщъьюя\\-"
    RU_SYMBOLS = RU_SYMBOLS_ONLY + RU_SYMBOLS_ONLY.upper()

    NON_WORD_SYMBOLS = [
        ".", ",", "?", "!", ":", ";", "???", "!!!", "!!", "...", "№", "„", "”", "“", "”", "«", "»",
        "%", "*", "-", "–", ")", "(", "[", "]", "{", "}", "/"
    ]

    ENGLISH_ALPHABET = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
        "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]

    UKRAINE_ALPHABET = [
        "а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "ї", "й", "к",
        "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ",
        "ь", "ю", "я"
    ]

    RUSSIAN_ALPHABET = [
        "а", "б", "в", "г", "д", "е", "ё", "э", "ж", "з", "ы", "и", "й", "к", "л",
        "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ",
        "ь", "ю", "я"
    ]

    ALPHABET = UKRAINE_ALPHABET


# Приклад використання

