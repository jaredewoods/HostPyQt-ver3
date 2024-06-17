from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject

class FlagStateManager(QObject):
    # This is used for the state manager view
    state_updated = pyqtSignal(str, bool, str)

    def __init__(self, signal_distributor):
        super().__init__()
        self.signal_distributor = signal_distributor

        self.serial_connected = False
        self.tcp_connected = False
        self.macro_ready_to_run = False
        self.macro_running = False
        self.macro_stopped = False
        self.macro_completed = False
        self.waiting_for_response = False
        self.response_received = False
        self.completion_received = False
        self.alarm_received = False
        self.debug_mode = False
        self.display_timestamp = False

        # Connect signal_distributor signal to the update_state method
        self.signal_distributor.state_changed.connect(self.update_state)

    @pyqtSlot(str, bool, str)
    def update_state(self, flag_name, value, condition):
        if not hasattr(self, flag_name):
            print(f"Unknown flag: {flag_name}")
            return

        current_value = getattr(self, flag_name)

        if condition == 'update':
            setattr(self, flag_name, value)
        elif condition == 'validate' and current_value != value:
            setattr(self, flag_name, value)
        elif condition == 'toggle':
            setattr(self, flag_name, not current_value)

        self.state_updated.emit(flag_name, getattr(self, flag_name), condition)
        print(f"Updated {flag_name} to {getattr(self, flag_name)}")

    def get_flag_status(self, flag_name):
        if hasattr(self, flag_name):
            return getattr(self, flag_name)
        else:
            raise AttributeError(f"Flag '{flag_name}' does not exist.")

class FlagStateView(QMainWindow):
    def __init__(self, flag_state_manager):
        super().__init__()
        self.flag_state_manager = flag_state_manager

        self.setWindowTitle("State Manager")
        self.setGeometry(100, 100, 300, 450)
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Flag", "Value", "Condition"])
        self.populate_table()

        self.flag_state_manager.state_updated.connect(self.update_table)

    def populate_table(self):
        flags = [
            "serial_connected", "tcp_connected", "macro_ready_to_run", "macro_running",
            "macro_stopped", "macro_completed", "waiting_for_response", "response_received",
            "completion_received", "alarm_received", "debug_mode", "display_timestamp"
        ]

        self.table_widget.setRowCount(len(flags))
        for row, flag in enumerate(flags):
            value = getattr(self.flag_state_manager, flag)
            self.table_widget.setItem(row, 0, QTableWidgetItem(flag))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
            self.table_widget.setItem(row, 2, QTableWidgetItem("Inactive"))

    @pyqtSlot(str, bool, str)
    def update_table(self, flag_name, value, update_condition):
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.item(row, 0).text() == flag_name:
                self.table_widget.setItem(row, 1, QTableWidgetItem(str(value)))
                condition_item = self.table_widget.item(row, 2)
                condition_item.setText(update_condition)
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)

                    # Set font color and background based on value
                    if value:
                        item.setForeground(QColor('white'))
                        item.setBackground(QColor('darkGreen'))
                    else:
                        item.setForeground(QColor('white'))
                        item.setBackground(QColor('darkRed'))
                break

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    state_manager = FlagStateManager()
    window = FlagStateView(state_manager)
    window.show()

    sys.exit(app.exec())
