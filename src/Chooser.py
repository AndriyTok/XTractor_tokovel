import os
from tkinter import Tk
from tkinter import filedialog

class Chooser:
    def __init__(self):
        # Ініціалізація вікна Tk, але його не показуємо
        self.root = Tk()
        self.root.withdraw()
        self.default_directory = "doc"  # Встановлюємо початкову директорію

    def get_file_to_save(self):
        # Вибір файлу для збереження
        file_path = filedialog.asksaveasfilename(initialdir=self.default_directory)
        return file_path if file_path else None

    def get_directory_path(self):
        # Вибір директорії
        directory_path = filedialog.askdirectory(initialdir=self.default_directory)
        return directory_path if directory_path else None

    def get_file_to_save_csv(self, suggested_file=None):
        # Вибір файлу для збереження у форматі .csv
        if suggested_file:
            initialfile = suggested_file
        else:
            initialfile = "output.csv"  # За замовчуванням назва для файлу

        file_path = filedialog.asksaveasfilename(
            initialdir=self.default_directory,
            initialfile=initialfile,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        return file_path if file_path else None

    def get_file_path(self):
        # Вибір файлу для відкриття
        file_path = filedialog.askopenfilename(initialdir=self.default_directory)
        return file_path if file_path else None

