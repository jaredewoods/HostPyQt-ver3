from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit, QMessageBox, QPushButton
from PyQt6.QtCore import pyqtSlot, QTimer
import sys
import os
from datetime import datetime

from serial_service.serial_model import SerialModel
from serial_service.serial_view import SerialView
from serial_service.serial_controller import SerialController
from tcp_service.tcp_model import TCPModel
from tcp_service.tcp_view import TCPView
from tcp_service.tcp_controller import TCPController
from macro_service.macro_model import MacroModel
from macro_service.macro_view import MacroView
from macro_service.macro_controller import MacroController
from macro_service.macro_executor import MacroExecutor
from command_service.command_model import CommandModel
from command_service.command_view import CommandView
from command_service.command_controller import CommandController

from status_service.status_view import StatusView
from status_service.signal_distributor import SignalDistributor
from status_service.flag_state_manager import FlagStateManager, FlagStateView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.signal_distributor = SignalDistributor()
        self.flag_state_manager = FlagStateManager(self.signal_distributor)
        self.macro_executor = MacroExecutor(self.signal_distributor, self.flag_state_manager)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.control_frame = QFrame()
        self.control_frame.setMaximumWidth(400)  # set Max Width 300 for PC, 400 for Mac
        self.control_layout = QVBoxLayout(self.control_frame)

        self.message_display_frame = QTabWidget()
        self.message_display_frame.setFixedWidth(400)
        self.log_display = QTextEdit()
        self.log_display.setStyleSheet("""
            QTextEdit {
                font-weight: bold;
                background-color: #002456;
                color: #F8F8F2; 
            }
        """)
        self.log_display.setReadOnly(True)
        self._debug_display = QTextEdit()
        self._debug_display.setReadOnly(True)
        self._debug_display.setStyleSheet("background-color: #060606; "
                                          "color: white;")
        self.message_display_frame.addTab(self.log_display, "Log")
        self.message_display_frame.addTab(self._debug_display, "Debug")
        self.message_display_frame.currentChanged.connect(self.on_tab_changed)

        self.serial_model = SerialModel(self.signal_distributor, self.flag_state_manager)
        self.serial_view = SerialView()
        self.serial_controller = SerialController(self.serial_model, self.serial_view, self.signal_distributor, self.flag_state_manager)
        self.tcp_model = TCPModel(self.signal_distributor)
        self.tcp_view = TCPView()
        self.tcp_controller = TCPController(self.tcp_model, self.tcp_view, self.signal_distributor)
        self.macro_model = MacroModel()
        self.macro_view = MacroView()
        self.macro_controller = MacroController(self.macro_model, self.macro_view, self.signal_distributor, self.flag_state_manager)
        self.command_view = CommandView(self.signal_distributor)
        self.command_model = CommandModel()
        self.command_controller = CommandController(self.command_model, self.command_view, self.signal_distributor)
        self.status_view = StatusView()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.serial_view, "Serial")
        self.tab_widget.addTab(self.tcp_view, "TCP / IP")
        self.tab_widget.addTab(self.macro_view, "Macro")
        self.control_layout.addWidget(self.tab_widget)
        self.control_layout.addWidget(self.status_view)
        self.control_layout.addWidget(self.command_view)

        self.main_layout.addWidget(self.control_frame)
        self.main_layout.addWidget(self.message_display_frame)
        self.setWindowTitle("Main Window")
        self.signal_distributor.DEBUG_MESSAGE.emit("MainWindow initialization complete")
        self.flag_state_view = FlagStateView(self.flag_state_manager)
        self.signal_distributor.DEBUG_MESSAGE.emit("FlagStateView initialization complete")
        self.flag_state_view.hide()

        self.xgx_command = None
        self.wait_command = None
        self.connect_signals()

        # Log message handling
        self.pending_log_messages = []
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.process_typewriter_log_message)
        self.typewriter_interval = 2  # Adjust for typewriter effect speed
        self.current_typewriter_message = ""
        self.current_typewriter_index = 0

    def connect_signals(self):
        self.signal_distributor.ALARM_MESSAGE.connect(self.show_alarm_messagebox)
        self.signal_distributor.CLEAR_FIELDS_SIGNAL.connect(self.command_view.clear_fields)
        self.signal_distributor.CLEAR_LOG_SIGNAL.connect(self.clear_log)
        self.signal_distributor.CONSTRUCT_COMMAND_SIGNAL.connect(self.command_controller.construct_command)
        self.signal_distributor.CURRENT_ITEM_SIGNAL.connect(self.macro_controller.receive_current_item)
        self.signal_distributor.DEBUG_MESSAGE.connect(self.update_debug_display)
        self.signal_distributor.FILTER_CONSTRUCTED_COMMAND_SIGNAL.connect(self.serial_model.filter_constructed_command)
        self.signal_distributor.ITEM_SELECTED_SIGNAL.connect(self.macro_controller.load_macro_sequence_line)
        self.signal_distributor.LOAD_COMMAND_INTO_VIEW.connect(self.command_view.set_command_details)
        self.signal_distributor.LOG_MESSAGE.connect(self.update_log_display)
        self.signal_distributor.MACRO_TRIGGER_SEQ00_SIGNAL.connect(self.macro_executor.seq00_start_cycle)
        self.signal_distributor.MACRO_TRIGGER_SEQ01_SIGNAL.connect(self.macro_executor.seq01_start_command)
        self.signal_distributor.MACRO_TRIGGER_SEQ02_SIGNAL.connect(self.macro_executor.seq02_waiting_for_completion)
        self.signal_distributor.MACRO_TRIGGER_SEQ03_SIGNAL.connect(self.macro_executor.seq03_handling_command_completion)
        self.signal_distributor.MACRO_TRIGGER_SEQ04_SIGNAL.connect(self.macro_executor.seq04_handling_cycle_completion)
        self.signal_distributor.NEXT_CYCLE_ITEM_SIGNAL.connect(self.command_view.select_next_macro_item)
        self.signal_distributor.REQUEST_CURRENT_ITEM_SIGNAL.connect(self.command_view.send_current_item)
        self.signal_distributor.REQUEST_TOTAL_CYCLES_SIGNAL.connect(self.provide_total_cycles)
        self.signal_distributor.RESET_BUTTON_CLICKED.connect(self.reset_macro)
        self.signal_distributor.RESTART_CYCLE_SIGNAL.connect(self.command_view.restart_cycle)
        self.signal_distributor.SEND_TOTAL_CYCLES_SIGNAL.connect(self.macro_executor.handle_total_cycles)
        self.signal_distributor.SET_CURRENT_ROW_SIGNAL.connect(self.command_view.set_current_row)
        self.signal_distributor.SINGLE_SHOT_BUTTON_CLICKED.connect(self.command_controller.send_single_shot)
        self.signal_distributor.STATE_UPDATED_SIGNAL.connect(self.flag_state_view.update_table)
        self.signal_distributor.STATE_UPDATED_SIGNAL.connect(self.on_state_changed)
        self.signal_distributor.TEXT_CHANGED_SIGNAL.connect(self.command_controller.handle_text_changed)
        self.signal_distributor.UPDATE_COMPLETED_CYCLES_SIGNAL.connect(self.macro_view.update_completed_cycles)
        self.signal_distributor.UPDATE_MACRO_COMMAND.connect(self.command_view.update_macro_sequence)
        self.signal_distributor.WAIT_COMMAND_EXECUTOR_SIGNAL.connect(self.handle_wait_command)
        self.signal_distributor.XGX_COMMAND_EXECUTOR_SIGNAL.connect(self.handle_xgx_command)
        self.signal_distributor.CYCLE_COMPLETED_SIGNAL.connect(self.command_controller.signal_cycle_completed)
        self.signal_distributor.EXPORT_LOG_BUTTON_SIGNAL.connect(self.export_log)

    @pyqtSlot()
    def export_log(self):
        logs_dir = os.path.join(os.getcwd(), 'LOGS')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        current_time = datetime.now().strftime('%m%d%Y%H%M%S')
        log_filename = f'{current_time}.txt'
        log_filepath = os.path.join(logs_dir, log_filename)

        log_text = self.log_display.toPlainText()

        with open(log_filepath, 'w') as log_file:
            log_file.write(log_text)

        self.signal_distributor.DEBUG_MESSAGE.emit(f"Log exported to {log_filepath}")

        # Show confirmation dialog
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Log Exported")
        msg_box.setText(f"Log has been exported to {log_filename}.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Close)
        msg_box.exec()

    @pyqtSlot()
    def clear_log(self):
        self.log_display.clear()

    @pyqtSlot()
    def reset_macro(self):
        self.macro_view.update_completed_cycles("0")
        self.command_view.macro_sequence_display.setCurrentRow(0)
        self.signal_distributor.DEBUG_MESSAGE.emit("resetting macro")
        self.status_view.start_label.setText("--:--:--")
        self.status_view.stop_label.setText("--:--:--")
        self.status_view.run_label.setText("--:--:--")

    @pyqtSlot()
    def provide_total_cycles(self):
        total_cycles = int(self.macro_view.macro_total_cycles_lbl.text())
        self.signal_distributor.SEND_TOTAL_CYCLES_SIGNAL.emit(total_cycles)

    @pyqtSlot(str, bool)
    def on_state_changed(self, flag_name, value):
        self._debug_display.append(f"State changed: {flag_name} -> {value}")
        _handler = getattr(self, f"handle_{flag_name}", None)
        if _handler:
            _handler(value)

    @pyqtSlot(bool)
    def handle_serial_connected(self, value):
        self._debug_display.append(f"Serial connection status: {value}")
        self.serial_controller.update_connection_state(value)
        self.status_view.update_serial_status(value)

    @pyqtSlot(bool)
    def handle_tcp_connected(self, value):
        self._debug_display.append(f"TCP connection status: {value}")
        self.tcp_controller.update_connection_btn_state(value)
        self.status_view.update_tcp_status(value)

    @pyqtSlot(bool)
    def handle_macro_ready_to_run(self, value):
        self._debug_display.append(f"Macro ready to run status: {value}")

    @pyqtSlot(bool)
    def handle_macro_running(self, value):
        self._debug_display.append(f"Macro running status: {value}")
        self.status_view.update_macro_status(value)
        if value:
            self.status_view.update_start_time()
        else:
            self.status_view.update_stop_time()
        self.macro_executor.seq_start_sequence()

    @pyqtSlot(bool)
    def handle_macro_stopped(self, value):
        self._debug_display.append(f"Macro stopped status: {value}")

    @pyqtSlot(bool)
    def handle_macro_completed(self, value):
        self._debug_display.append(f"Macro completed status: {value}")

    @pyqtSlot(bool)
    def handle_waiting_for_response(self, value):
        self._debug_display.append(f"Waiting for response status: {value}")

    @pyqtSlot(bool)
    def handle_response_received(self, value):
        self._debug_display.append(f"Response received status: {value}")

    @pyqtSlot(bool)
    def handle_completion_received(self, value):
        self._debug_display.append(f"Completion received status: {value}")

    @pyqtSlot(bool)
    def handle_alarm_received(self, value):
        self._debug_display.append(f"Alarm received status: {value}")

    @pyqtSlot(bool)
    def handle_debug_mode(self, value):
        self._debug_display.append(f"Debug mode status: {value}")
        self.command_view.debug_display_update(value)

    @pyqtSlot(bool)
    def handle_display_timestamp(self, value):
        self._debug_display.append(f"Display timestamp status: {value}")

    @pyqtSlot(str)
    def handle_wait_command(self, command):
        self.macro_executor.response_timer.stop()
        self.wait_command = command[6:10]
        self.command_controller.handle_wait_command(self.wait_command)

    @pyqtSlot(str)
    def handle_xgx_command(self, command):
        self.xgx_command = command[6:8]
        self.tcp_controller.handle_tcp_command(self.xgx_command)
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Handling XG-X command: {self.xgx_command}")

    @pyqtSlot(str)
    def update_debug_display(self, message):
        self._debug_display.append(message)

    @pyqtSlot(str)
    def update_log_display(self, message):
        self.pending_log_messages.append(message)
        if not self.typewriter_timer.isActive():
            self.typewriter_timer.start(self.typewriter_interval)

    @pyqtSlot()
    def process_typewriter_log_message(self):
        if self.current_typewriter_message == "" and self.pending_log_messages:
            self.current_typewriter_message = self.pending_log_messages.pop(0)
            self.current_typewriter_index = 0

        if self.current_typewriter_index < len(self.current_typewriter_message):
            self.log_display.insertPlainText(self.current_typewriter_message[self.current_typewriter_index])
            self.current_typewriter_index += 1
        else:
            self.log_display.append('')  # Move to the next line after the typewriter message
            self.current_typewriter_message = ""
            if not self.pending_log_messages:
                self.typewriter_timer.stop()

    @staticmethod
    def show_alarm_messagebox(alarm_code, subcode):
        from application_ui.alarm_message_box import AlarmMessageBox
        AlarmMessageBox.show_alarm_messagebox(alarm_code, subcode)

    @pyqtSlot(int)
    def on_tab_changed(self, index):
        # Check if the debug tab is selected
        if self.message_display_frame.tabText(index) == "Debug":
            self.flag_state_view.show()
            self.signal_distributor.STATE_UPDATED_SIGNAL.emit("debug_mode", True)
        else:
            self.flag_state_view.hide()
            self.signal_distributor.STATE_UPDATED_SIGNAL.emit("debug_mode", False)
