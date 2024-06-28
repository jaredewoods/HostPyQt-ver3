# signal_distributor.py
"""Define signals that will be used across the application.
Emit signals when events are triggered."""

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):
    ITEM_SELECTED_SIGNAL = pyqtSignal()
    SINGLE_SHOT_BUTTON_CLICKED = pyqtSignal()
    RESET_BUTTON_CLICKED = pyqtSignal()
    RUN_NEXT_COMMAND_SIGNAL = pyqtSignal()
    STATE_UPDATED_SIGNAL = pyqtSignal(str, bool)
    LOAD_COMMAND_INTO_VIEW = pyqtSignal(str, str, str)
    REQUEST_CURRENT_ITEM_SIGNAL = pyqtSignal()
    RECEIVE_CURRENT_ITEM_SIGNAL = pyqtSignal(str)
    CURRENT_ITEM_SIGNAL = pyqtSignal(str)
    CLEAR_FIELDS_SIGNAL = pyqtSignal()
    SET_CURRENT_ROW_SIGNAL = pyqtSignal(int)
    TEXT_CHANGED_SIGNAL = pyqtSignal()
    STATE_CHANGED_SIGNAL = pyqtSignal(str, bool)
    REQUEST_TOTAL_CYCLES_SIGNAL = pyqtSignal()
    SEND_TOTAL_CYCLES_SIGNAL = pyqtSignal(int)
    UPDATE_COMPLETED_CYCLES_SIGNAL = pyqtSignal(int)
    RESTART_CYCLE_SIGNAL = pyqtSignal()
    CYCLE_COMPLETED_SIGNAL = pyqtSignal()
    UPDATE_MACRO_COMMAND = pyqtSignal(str)

    WAIT_COMMAND_EXECUTOR_SIGNAL = pyqtSignal(str)
    XGX_COMMAND_EXECUTOR_SIGNAL = pyqtSignal(str)
    CONSTRUCT_COMMAND_SIGNAL = pyqtSignal()
    FILTER_CONSTRUCTED_COMMAND_SIGNAL = pyqtSignal(str)

    NEXT_CYCLE_ITEM_SIGNAL = pyqtSignal()
    MACRO_TRIGGER_SEQ00_SIGNAL = pyqtSignal()
    MACRO_TRIGGER_SEQ01_SIGNAL = pyqtSignal()
    MACRO_TRIGGER_SEQ02_SIGNAL = pyqtSignal()
    MACRO_TRIGGER_SEQ03_SIGNAL = pyqtSignal()
    MACRO_TRIGGER_SEQ04_SIGNAL = pyqtSignal()

    DEBUG_MESSAGE = pyqtSignal(str)
    LOG_MESSAGE = pyqtSignal(str)
    ALARM_MESSAGE = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def emit_state_change(self, flag_name, value, update_condition):
        self.STATE_CHANGED_SIGNAL.emit(flag_name, value, update_condition)
