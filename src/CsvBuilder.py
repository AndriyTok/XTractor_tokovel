class CsvBuilder:
    NEW_LINE = "\n"

    def __init__(self, delimiter):
        self.sb = []
        self.delimiter = delimiter
        self.is_on = True

    def add(self, obj):
        self._delimite(force=False)
        self._append(obj)
        return self

    def add_with_offset(self, offset, obj):
        for _ in range(offset):
            self._delimite(force=True)
        self._append(obj)
        return self

    def new_line(self, count=1):
        for _ in range(count):
            self._append(self.NEW_LINE)
        return self

    def _delimite(self, force):
        if (self.sb and not self.sb[-1].endswith(self.NEW_LINE)) or force:
            self.sb.append(self.delimiter)

    def _append(self, obj):
        if self.is_on:
            self.sb.append(str(obj))

    def __str__(self):
        return ''.join(self.sb)

    def turn_off(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

