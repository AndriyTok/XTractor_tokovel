from enum import Enum

class ValueType(Enum):

    N_VALUE = "N_VALUE"
    F_VALUE = "F_VALUE"
    S_VALUE = "S_VALUE"
    SS_VALUE = "SS_VALUE"
    L_VALUE = "L_VALUE"

class Node:
    def __init__(self, level, index, title, value_type=None, child_list=None):
        self.level = level
        self.index = index
        self.title = title
        self.value_type = value_type
        self.child_list = child_list if child_list else []
        self.selected_child = None
        self.value = None

    def get_level(self):
        return "None"

    def get_target(self):
        return "None"

    def get_sub_level(self):
        return "None"

    def is_valuable(self):
        return self.selected_child and self.selected_child.value_type is not None