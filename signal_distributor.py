# signal_distributor.py
"""Define signals that will be used across the application.
Emit signals when events are triggered."""

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):
    state_changed = pyqtSignal(str, bool, str)

    def __init__(self):
        super().__init__()
