import os
import chardet  # бібліотека для виявлення кодування
import codecs


class IOUtils:

    @staticmethod
    def folder_size(directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def read_file_by_charset(path, encoding):
        with open(path, 'rb') as f:
            content = f.read()
        return content.decode(encoding)

    @staticmethod
    def read_file(path):
        with open(path, 'rb') as f:
            content = f.read()

        detected_encoding = IOUtils.detect_encoding(content)
        if detected_encoding is None:
            detected_encoding = "utf-8"

        try:
            return content.decode(detected_encoding)
        except (UnicodeDecodeError, LookupError):
            return ""

    @staticmethod
    def detect_encoding(content):
        result = chardet.detect(content)
        encoding = result['encoding']
        if encoding is None:
            encoding = "utf-8"
        return encoding

    @staticmethod
    def write_file(text, file_full_name):
        encoding = IOUtils.detect_encoding(text.encode())
        with codecs.open(file_full_name, 'w', encoding=encoding) as f:
            f.write(text)

