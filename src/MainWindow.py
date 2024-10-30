import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.m_path = None  # Зберігає шлях до обраного файлу
        self.setWindowTitle("Text Analyzer")

        # Ініціалізація інтерфейсу
        self.init_ui()

    def init_ui(self):
        # Основний текстовий лейбл для виводу результатів
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)  # Робимо поле тільки для читання

        # Основний лейбл з описом
        self.label = QLabel("Choose a file to analyze", self)
        self.label.setAlignment(Qt.AlignCenter)

        # Кнопка для вибору файлу
        self.file_button = QPushButton("Choose File", self)
        self.file_button.clicked.connect(self.choose_file)

        # Кнопка для запуску аналізу
        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.clicked.connect(self.analyze)

        # Компонуємо всі елементи
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.analyze_button)
        self.layout.addWidget(self.result_display)

        # Задаємо layout для центрального віджету
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def choose_file(self):
        # Відкриття діалогу для вибору файлу
        file_dialog = QFileDialog(self)
        file_dialog.setDirectory(".data")  # Відкрити діалог в .data
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "TXT files(*.txt);;CSV Files (*.csv);;All Files (*)")

        if file_path:
            # Встановлення обраного шляху до файлу
            file_name = os.path.basename(file_path)
            self.m_path = os.path.join(".data", file_name)
            self.label.setText(f"Selected file: {self.m_path}")

    def analyze(self):
        # Перевіряємо, чи вибрано файл
        if not self.m_path:
            self.label.setText("No file selected!")
            return

        # Шлях до Main.py
        main_py_path = "main.py"

        # Конструюємо команду для запуску Main.py з обраним файлом
        cmd = f"python3 {main_py_path} {self.m_path.replace('\\', '/')}"

        try:
            # Запускаємо процес та чекаємо на завершення
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Відображення результатів
            if stderr:
                self.result_display.setPlainText(f"Error occurred:\n{stderr.decode()}")
            else:
                self.result_display.setPlainText(stdout.decode())  # Виводимо результат аналізу

        except Exception as e:
            self.result_display.setPlainText(f"An error occurred: {str(e)}")

