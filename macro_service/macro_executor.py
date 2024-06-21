from PyQt6.QtCore import pyqtSignal


class MacroExecutor(QObject):
    start_signal = pyqtSignal()

    def __init__(self, macro_sequence):
        super().__init__()
        self.macro_sequence = macro_sequence
        self.current_cycle = 0
        print(f"Current Cycle = {current_cycle}")

