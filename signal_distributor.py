# signal_distributor.py
"""Define signals that will be used across the application.
Emit signals when events are triggered."""

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):
    state_changed = pyqtSignal(str, bool, str)
    REQUEST_TOTAL_CYCLES_SIGNAL = pyqtSignal()
    SEND_TOTAL_CYCLES_SIGNAL = pyqtSignal(int)
    updateCompletedCycles = pyqtSignal(int)

    construct_command_signal = pyqtSignal()
    wait_command_executor = pyqtSignal(str)
    xgx_command_executor = pyqtSignal(str)
    filter_constructed_command = pyqtSignal(str)

    next_macro_item = pyqtSignal()
    macro_trigger_seq00 = pyqtSignal()
    macro_trigger_seq01 = pyqtSignal()
    macro_trigger_seq02 = pyqtSignal()
    macro_trigger_seq03 = pyqtSignal()
    macro_trigger_seq04 = pyqtSignal()
    restart_cycle = pyqtSignal()

    def __init__(self):
        super().__init__()

    def emit_state_change(self, flag_name, value, update_condition):
        self.state_changed.emit(flag_name, value, update_condition)
