# signal_distributor.py
"""Define signals that will be used across the application.
Emit signals when events are triggered."""

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):
    state_changed = pyqtSignal(str, bool, str)
    send_command_signal = pyqtSignal()  # Add this line to define the new signal

    def __init__(self):
        super().__init__()

    def emit_state_change(self, flag_name, value, update_condition):
        self.state_changed.emit(flag_name, value, update_condition)
