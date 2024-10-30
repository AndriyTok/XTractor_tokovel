import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.Shared import Node, ValueType
from src.Chooser import Chooser
from src.Constants import Constants
from src.CsvBuilder import CsvBuilder
from src.IOUtils import IOUtils
from src.Mode import Mode



class MainWindow:
    def __init__(self, root):
        self.panel = None
        self.root = root
        self.root.title("Xtractor 2.0")
        self.root.geometry("1200x400")

        self.mode = Mode()
        self.m_current_node = Node(0, 0, "Root", child_list=[
            Node(1, 0, "Позначити позиціі всіх", child_list=[
                Node(2, 0, "символів", child_list=[
                    Node(3, 0, "що відповідають символу", ValueType.S_VALUE)
                ]),
                Node(2, 1, "символьних нграм", ValueType.N_VALUE)
            ])
        ])

        # Меню
        self.menu_bar = tk.Menu(root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Відкрити", command=self.open_new)
        file_menu.add_command(label="Convert 10010.. to dt", command=self.convert)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)
        root.config(menu=self.menu_bar)

        # Вкладки
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill='both')

        # Панель вибору файлу
        self.lbl_path = tk.Label(root, text="Файл не вибрано")
        self.lbl_path.pack()

        self.result_text = tk.Text(root, wrap='word')
        self.result_text.pack()

        # Кнопка "Отримати результат"
        self.btn_analyze = tk.Button(root, text="Отримати результат", command=self.analyze)
        self.btn_analyze.pack(side=tk.BOTTOM)

        # Кнопка "Зберегти"
        self.btn_save = tk.Button(root, text="Зберегти", command=self.save, state=tk.DISABLED)
        self.btn_save.pack(side=tk.BOTTOM)

    def open_new(self):
        chooser = Chooser()
        file_path = chooser.get_file_path()
        if file_path:
            self.lbl_path.config(text=file_path)
            self.m_path = file_path
            self.m_text = IOUtils.read_file(file_path)

    def convert(self):
        chooser = Chooser()
        file_path = chooser.get_file_path()
        if file_path:
            separator = messagebox.askstring("Розділювач", "Вкажіть розділювач")
            if not separator:
                separator = ","
            text = IOUtils.read_file(file_path)
            numbers = text.split(separator)
            indexes = [i for i, num in enumerate(numbers) if num.strip() == "1"]
            distances = self.get_distances(indexes)
            IOUtils.write_file(','.join(map(str, distances)), chooser.get_file_to_save_csv())

    def analyze(self):
        try:
            self.read_mode()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            return

        if not self.mode:
            return

        command = f"python Main.py -i {self.m_path} -L {self.mode.get_level()} -T {self.mode.get_target()} -S {self.mode.get_sub_level()} " \
                  f"-s {self.mode.get_target_string()} -ff {self.mode.get_frequency_from()} -ft {self.mode.get_frequency_to()} " \
                  f"-ss {self.mode.get_stop_symbols()} -n {self.mode.get_n()} -l {self.mode.get_l()}"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = process.communicate()
        if err:
            print("Помилка виконання:", err)
        else:
            print("Результат:", out)

        self.display_results()

    def save(self):
        chooser = Chooser()
        if self.tab_control.index("current") == 0:
            IOUtils.write_file(self.binar_result, chooser.get_file_to_save_csv("Bin_" + self.mode.phrase + ".csv"))
        elif self.tab_control.index("current") == 1:
            IOUtils.write_file(self.distances_result, chooser.get_file_to_save_csv("Dt_" + self.mode.phrase + ".csv"))

    def read_mode(self):
        self.mode = Mode()
        code_list = []
        sb = []
        last_node = None

        for i, box in enumerate(self.panel.winfo_children()):
            combo = box.winfo_children()[0]
            node = self.node_map.get(combo.winfo_id())

            if node.get_selection() is not None:
                code_list.append(node.get_selection().index)
                sb.append(f"{node.get_selection().title} ")

            if len(box.winfo_children()) > 1:
                if node.get_selection().get_value_type() == ValueType.F_VALUE:
                    l_from = box.winfo_children()[1]
                    tf_from = box.winfo_children()[2]
                    value_from = tf_from.get().strip()

                    l_to = box.winfo_children()[3]
                    tf_to = box.winfo_children()[4]
                    value_to = tf_to.get().strip()

                    sb.append(f"{l_from.cget('text')} {value_from} {l_to.cget('text')} {value_to} ")

                    if value_from and value_to:
                        if node.is_valuable():
                            self.mode.value_map[node.get_selection().value_type] = f"{value_from}:{value_to}"
                        else:
                            raise Exception("Node is not valuable but contains textfield")
                else:
                    tf = box.winfo_children()[1]
                    value = tf.get()

                    if node.get_selection().get_value_type() in {ValueType.SS_VALUE, ValueType.S_VALUE}:
                        value = value.replace(" ", "$space$")

                    if node.get_selection().get_value_type() != ValueType.SS_VALUE:
                        sb.append(f"{value} ")

                    value = value.strip()

                    if value:
                        if node.is_valuable():
                            self.mode.value_map[node.get_selection().value_type] = value
                        else:
                            raise Exception("Node is not valuable but contains textfield")

            last_node = node

        self.mode.code = code_list
        self.mode.phrase = ''.join(sb)
        self.mode.last_node = last_node.get_selection() if last_node.get_selection() else last_node
        return ''.join(sb)

    def display_results(self):
        # Метод для відображення результатів у вкладках
        self.binar_result = IOUtils.read_file("raw.csv")
        self.distances_result = IOUtils.read_file("dt.csv")
        self.found_result = IOUtils.read_file("val.csv")
        self.print_result = IOUtils.read_file("found.csv")

        # Очистка вкладок і додавання нових результатів
        self.tab_control.forget("all")
        if self.binar_result:
            self.add_result_tab("10010...", self.binar_result[:20000])
        if self.distances_result:
            self.add_result_tab("dt", self.distances_result[:20000])

    def add_result_tab(self, title, content):
        frame = tk.Frame(self.tab_control)
        text_area = tk.Text(frame, wrap='word')
        text_area.insert(tk.END, content)
        text_area.pack(expand=1, fill='both')
        self.tab_control.add(frame, text=title)

    def get_distances(self, indexes):
        distances = [indexes[0]]
        for i in range(1, len(indexes)):
            distances.append(indexes[i] - indexes[i - 1] - 1)
        return distances

# Ініціалізація головного вікна програми
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
