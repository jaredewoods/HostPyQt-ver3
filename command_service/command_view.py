import os
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox, QLineEdit, QLabel, \
    QPushButton, QListWidgetItem
from PyQt6.QtCore import Qt
from resources.command_dictionary import commands
import sys


class CommandView(QWidget):

    def __init__(self, signal_distributor):
        super().__init__()
        self.stop_sequence_btn = None
        self.start_sequence_btn = None
        self.export_btn = None
        self.clear_log_btn = None
        self.next_step_btn = None
        self.reset_sequence_btn = None
        self.single_shot_btn = None
        self.macro_sequence_display = None
        self.macro_display_layout = None
        self.display_command = None
        self.dropdown_code = None
        self.dropdown_unit_no = None
        self.entry_parameters = None
        self.carriage_return_checkbox = None
        self.checksum_checkbox = None
        self.start_bit_checkbox = None
        self.signal_distributor = signal_distributor
        self.main_layout = QVBoxLayout()

        self.setup_macro_display()
        self.setup_display_line()
        self.setup_dropdowns_and_parameters()
        self.setup_checkboxes()
        self.setLayout(self.main_layout)

    @pyqtSlot(int)
    def set_current_row(self, row):
        if self.macro_sequence_display.count() > 0:
            self.macro_sequence_display.setCurrentRow(row)

    def setup_checkboxes(self):
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.setContentsMargins(20, 0, 0, 0)
        checkboxes_layout.setSpacing(10)

        self.start_bit_checkbox = QCheckBox("Start Bit")
        self.checksum_checkbox = QCheckBox("Checksum")
        self.carriage_return_checkbox = QCheckBox("<CR>")

        self.start_bit_checkbox.setChecked(True)
        self.checksum_checkbox.setChecked(True)
        self.carriage_return_checkbox.setChecked(True)

        self.start_bit_checkbox.hide()
        self.checksum_checkbox.hide()
        self.carriage_return_checkbox.hide()

        checkboxes_layout.addWidget(self.start_bit_checkbox)
        checkboxes_layout.addWidget(self.checksum_checkbox)
        checkboxes_layout.addWidget(self.carriage_return_checkbox)
        self.main_layout.addLayout(checkboxes_layout)

    def setup_dropdowns_and_parameters(self):
        dropdowns_layout = QHBoxLayout()
        self.dropdown_unit_no = QComboBox()
        self.dropdown_unit_no.addItems(["", "1", "2"])
        self.dropdown_unit_no.setStyleSheet("""
            QComboBox {
                background-color: #002456;
                color: #F8F8F2;
                font-weight: bold;
                padding: 4px;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(noarrow.png);  /* Optional: You can set an image for the dropdown arrow */
            }
            QComboBox QAbstractItemView::item {
                text-align: center;
            }
        """)
        self.dropdown_code = QComboBox()
        self.dropdown_code.setEditable(True)
        self.dropdown_code.setStyleSheet("""
            QComboBox {
                background-color: #002456;
                color: #F8F8F2;
                font-weight: bold;
                padding: 4px;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(noarrow.png);  /* Optional: You can set an image for the dropdown arrow */
            }
            QComboBox QAbstractItemView::item {
                text-align: center;
            }
        """)
        dropdowns_layout.addWidget(self.dropdown_unit_no)

        self.dropdown_code.addItem("")
        for command in commands.keys():
            self.dropdown_code.addItem(command)

        dropdowns_layout.addWidget(self.dropdown_code)

        self.entry_parameters = QLineEdit()
        self.entry_parameters.setFixedWidth(90)
        self.entry_parameters.setStyleSheet("""
            QLineEdit {
                background-color: #002456;
                color: #F8F8F2;
                font-weight: bold;
                padding: 4px;
            }
        """)
        dropdowns_layout.addWidget(self.entry_parameters)
        self.main_layout.addLayout(dropdowns_layout)

        self.dropdown_unit_no.hide()
        self.dropdown_code.hide()
        self.entry_parameters.hide()

    def setup_display_line(self):
        display_layout = QHBoxLayout()
        self.display_command = QLabel()
        self.display_command.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_command.setStyleSheet("""background-color: white; 
                                          color: #002456;
                                          font-size: 18px;
                                          font-weight: bold; 
                                          padding: 5px;
                                          border-width: 2px;
                                          border-style: solid;
                                          border-color: grey;                                          
                                          border-radius: 10px;""")
        display_layout.addWidget(self.display_command)
        self.main_layout.addLayout(display_layout)

    def setup_macro_display(self):
        self.macro_display_layout = QHBoxLayout()
        self.macro_sequence_display = QListWidget()
        self.macro_sequence_display.setStyleSheet("""
            QListWidget {
                font-weight: bold; 
                font-size: 12px;
                background-color: #002456;
                color: #F8F8F2;
            }
            QListWidget::item:selected {
                font-weight: bold; 
                background-color: #F8F8F2;
                color: #002456;
            }
        """)
        self.macro_sequence_display.itemSelectionChanged.connect(self.emit_item_selected)
        self.macro_display_layout.addWidget(self.macro_sequence_display)
        self.macro_sequence_display.setDisabled(True)

        # Create buttons layout
        buttons_layout = QVBoxLayout()
        self.start_sequence_btn = QPushButton("Start Sequence")
        self.stop_sequence_btn = QPushButton("Stop Sequence")
        self.reset_sequence_btn = QPushButton("Reset Sequence")
        self.single_shot_btn = QPushButton("Single Shot")
        self.next_step_btn = QPushButton("Next Step")
        self.clear_log_btn = QPushButton("Clear Log")
        self.export_btn = QPushButton("Export Log")

        # Add buttons to layout
        buttons_layout.addWidget(self.start_sequence_btn)
        self.start_sequence_btn.clicked.connect(self.set_macro_running_true)
        buttons_layout.addWidget(self.stop_sequence_btn)
        self.stop_sequence_btn.clicked.connect(self.set_macro_running_false)
        buttons_layout.addWidget(self.reset_sequence_btn)
        self.reset_sequence_btn.clicked.connect(self.signal_distributor.RESET_BUTTON_CLICKED)
        buttons_layout.addWidget(self.single_shot_btn)
        self.single_shot_btn.clicked.connect(self.signal_distributor.SINGLE_SHOT_BUTTON_CLICKED)
        buttons_layout.addWidget(self.next_step_btn)
        self.next_step_btn.clicked.connect(self.next_sequence_step)
        buttons_layout.addWidget(self.clear_log_btn)
        self.clear_log_btn.clicked.connect(self.signal_distributor.CLEAR_LOG_SIGNAL)
        buttons_layout.addWidget(self.export_btn)
        self.export_btn.clicked.connect(self.signal_distributor.EXPORT_LOG_BUTTON_SIGNAL.emit)
        self.macro_display_layout.addLayout(buttons_layout)
        self.main_layout.addLayout(self.macro_display_layout)

    def set_macro_running_true(self):
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_running", True)

    def set_macro_running_false(self):
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_running", False)

    @pyqtSlot()
    def select_next_macro_item(self):
        self.signal_distributor.DEBUG_MESSAGE.emit("selecting next macro item in CommandView")
        selected_items = self.macro_sequence_display.selectedItems()

        if selected_items:
            current_index = self.macro_sequence_display.row(selected_items[0])
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Current Index: {current_index}")
            next_index = current_index + 1
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Next Index: {next_index}")
            self.signal_distributor.DEBUG_MESSAGE.emit(
                f"Macro Sequence Display Count: {self.macro_sequence_display.count()}")
            if next_index < self.macro_sequence_display.count():
                self.macro_sequence_display.setCurrentRow(next_index)
                self.signal_distributor.MACRO_TRIGGER_SEQ01_SIGNAL.emit()
            else:
                self.signal_distributor.CYCLE_COMPLETED_SIGNAL.emit()

    @pyqtSlot()
    def restart_cycle(self):
        self.macro_sequence_display.setCurrentRow(0)
        self.signal_distributor.MACRO_TRIGGER_SEQ00_SIGNAL.emit()
        self.signal_distributor.DEBUG_MESSAGE.emit("Restarting Cycle")

    @pyqtSlot()
    def on_single_shot_btn_clicked(self):
        self.signal_distributor.SINGLE_SHOT_BUTTON_CLICKED.emit()

    @pyqtSlot()
    def emit_item_selected(self):
        self.signal_distributor.ITEM_SELECTED_SIGNAL.emit()

    @pyqtSlot(str)
    def update_macro_sequence(self, sequence):
        self.macro_sequence_display.clear()
        for item in sequence.split('\n'):
            self.macro_sequence_display.addItem(QListWidgetItem(item))

    @pyqtSlot()
    def next_sequence_step(self):
        self.signal_distributor.DEBUG_MESSAGE.emit("selecting next macro item in CommandView")
        selected_items = self.macro_sequence_display.selectedItems()
        if selected_items:
            current_index = self.macro_sequence_display.row(selected_items[0])
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Current Index: {current_index}")
            next_index = (current_index + 1) % self.macro_sequence_display.count()
            self.macro_sequence_display.setCurrentRow(next_index)

    @pyqtSlot(str)
    def set_command(self, command):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Command set: {command}")
        self.display_command.setText(command)

    @pyqtSlot(str)
    def set_unit_number(self, unit_number):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Unit number set: {unit_number}")  # Debug statement
        index = self.dropdown_unit_no.findText(str(unit_number))
        if index != -1:
            self.dropdown_unit_no.setCurrentIndex(index)

    @pyqtSlot(str)
    def set_parameters(self, parameters):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Parameters set: {parameters}")
        self.entry_parameters.setText(parameters)

    @pyqtSlot(str)
    def set_code(self, code):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Code set: {code}")
        index = self.dropdown_code.findText(code)
        if index != -1:
            self.dropdown_code.setCurrentIndex(index)
        else:
            self.dropdown_code.setCurrentText(code)

    @pyqtSlot()
    def clear_fields(self):
        self.set_unit_number("")
        self.set_code("")
        self.set_parameters("")
        # self.macro_sequence_display.clear()
        self.signal_distributor.DEBUG_MESSAGE.emit("Fields have been cleared")

    @pyqtSlot(str, str, str)
    def set_command_details(self, command, unit, parameters):
        self.signal_distributor.DEBUG_MESSAGE.emit(
            f"Setting command details: command={command}, unit={unit}, parameters={parameters}")
        self.set_command(command)
        self.set_unit_number(unit)
        self.set_parameters(parameters)
        self.set_code(command)
        self.signal_distributor.TEXT_CHANGED_SIGNAL.emit()

    @pyqtSlot()
    def send_current_item(self):
        selected_item = self.macro_sequence_display.currentItem()
        if selected_item:
            self.signal_distributor.CURRENT_ITEM_SIGNAL.emit(selected_item.text())

    @pyqtSlot(bool)
    def debug_display_update(self, value):
        if value:
            self.dropdown_unit_no.show()
            self.dropdown_code.show()
            self.entry_parameters.show()
            self.start_bit_checkbox.show()
            self.checksum_checkbox.show()
            self.carriage_return_checkbox.show()
        else:
            self.dropdown_unit_no.hide()
            self.dropdown_code.hide()
            self.entry_parameters.hide()
            self.start_bit_checkbox.hide()
            self.checksum_checkbox.hide()
            self.carriage_return_checkbox.hide()
