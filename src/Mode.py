from enum import Enum
from src.Shared import Node, ValueType # Імпорт класу Node із MainWindow

class Mode:
    def __init__(self):
        self.value_map = {}
        self.code = []
        self.last_node = Node(level=0, index=0, title="")  # Ініціалізуємо last_node як екземпляр Node
        self.phrase = ""

    def get_single_code(self):
        return ''.join(str(c) for c in self.code)

    def get_frequency_from(self):
        v = self.value_map.get(ValueType.F_VALUE)
        if v is not None:
            return int(v.split(":")[0])
        return -1

    def get_frequency_to(self):
        v = self.value_map.get(ValueType.F_VALUE)
        if v is not None:
            return int(v.split(":")[1])
        return -1

    def get_n(self):
        v = self.value_map.get(ValueType.N_VALUE)
        if v is not None:
            return int(v)
        return -1

    def get_l(self):
        v = self.value_map.get(ValueType.L_VALUE)
        if v is not None:
            return int(v)
        return -1

    def get_stop_symbols(self):
        return self.value_map.get(ValueType.SS_VALUE, "None")

    def get_target_string(self):
        return self.value_map.get(ValueType.S_VALUE, "None")

    def get_level(self):
        return self.last_node.get_level()

    def get_target(self):
        return self.last_node.get_target()

    def get_sub_level(self):
        return self.last_node.get_sub_level()
