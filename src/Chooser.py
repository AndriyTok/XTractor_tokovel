import os
from tkinter import Tk
from tkinter import filedialog

class Chooser:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()  # Prevents the root window from appearing
        self.default_directory = "doc"  # Set the initial directory

    def get_root(self):
        return self.root  # Return the root Tk window

    def get_file_to_save(self):
        # Select a file for saving
        file_path = filedialog.asksaveasfilename(initialdir=self.default_directory)
        return file_path if file_path else None

    def get_directory_path(self):
        # Select a directory
        directory_path = filedialog.askdirectory(initialdir=self.default_directory)
        return directory_path if directory_path else None

    def get_file_to_save_csv(self, suggested_file=None):
        # Select a file for saving as .csv
        initialfile = suggested_file or "output.csv"  # Default filename
        file_path = filedialog.asksaveasfilename(
            initialdir=self.default_directory,
            initialfile=initialfile,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        return file_path if file_path else None

    def get_file_path(self):
        # Select a file to open
        file_path = filedialog.askopenfilename(initialdir=self.default_directory)
        return file_path if file_path else None
