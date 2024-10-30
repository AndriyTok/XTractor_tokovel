from src.MainWindow import MainWindow

class Mode:
    @staticmethod
    def __init__(self):
        self.lastNode = None
        self.value_map = {}
        self.code = []
        self.last_node = MainWindow.Node()
        self.phrase = ""

    @staticmethod
    def get_single_code(self):
        return ''.join(str(c) for c in self.code)

    @staticmethod
    def get_frequency_from(self):
        v = self.value_map.get(MainWindow.ValueType.F_VALUE)
        if v is not None:
            return int(v.split(":")[0])
        return -1

    @staticmethod
    def get_frequency_to(self):
        v = self.value_map.get(MainWindow.ValueType.F_VALUE)
        if v is not None:
            return int(v.split(":")[1])
        return -1

    @staticmethod
    def get_n(self):
        v = self.value_map.get(MainWindow.ValueType.N_VALUE)
        if v is not None:
            return int(v)
        return -1

    @staticmethod
    def get_l(self):
        v = self.value_map.get(MainWindow.ValueType.L_VALUE)
        if v is not None:
            return int(v)
        return -1

    @staticmethod
    def get_stop_symbols(self):
        return self.value_map.get(MainWindow.ValueType.SS_VALUE, "None")

    @staticmethod
    def get_target_string(self):
        return self.value_map.get(MainWindow.ValueType.S_VALUE, "None")

    @staticmethod
    def get_level(self):
        return self.last_node.get_level()

    @staticmethod
    def get_target(self):
        return self.last_node.get_target()

    @staticmethod
    def get_sub_level(self):
        return self.last_node.get_sub_level()

