from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QComboBox, QLineEdit, QLabel, QPushButton, QListWidgetItem
from PyQt6.QtCore import Qt
from resources.command_dictionary import commands

class CommandView(QWidget):

    def __init__(self, signal_distributor):
        super().__init__()
        self.entry_parameters = None
        self.clear_btn = None
        self.edit_btn = None
        self.reset_btn = None
        self.single_shot_btn = None
        self.macro_sequence_display = None
        self.macro_display_layout = None
        self.display_command = None
        self.dropdown_code = None
        self.dropdown_unit_no = None
        self.carriage_return_checkbox = None
        self.checksum_checkbox = None
        self.start_bit_checkbox = None
        self.signal_distributor = signal_distributor
        self.main_layout = QVBoxLayout()
        self.is_editing = False

        self.setup_dropdowns_and_parameters()
        self.setup_checkboxes()
        self.setup_display_line()
        self.setup_macro_display()

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
        checkboxes_layout.addWidget(self.start_bit_checkbox)
        checkboxes_layout.addWidget(self.checksum_checkbox)
        checkboxes_layout.addWidget(self.carriage_return_checkbox)
        self.main_layout.addLayout(checkboxes_layout)

    def setup_dropdowns_and_parameters(self):
        dropdowns_layout = QHBoxLayout()
        self.dropdown_unit_no = QComboBox()
        self.dropdown_unit_no.addItems(["", "1", "2"])
        self.dropdown_code = QComboBox()
        self.dropdown_code.setEditable(True)
        dropdowns_layout.addWidget(QLabel("Unit No"))
        dropdowns_layout.addWidget(self.dropdown_unit_no)
        dropdowns_layout.addWidget(QLabel("Command"))

        self.dropdown_code.addItem("")
        for command in commands.keys():
            self.dropdown_code.addItem(command)

        dropdowns_layout.addWidget(self.dropdown_code)

        self.entry_parameters = QLineEdit()
        self.entry_parameters.setFixedWidth(90)
        dropdowns_layout.addWidget(QLabel("Param."))
        dropdowns_layout.addWidget(self.entry_parameters)
        self.main_layout.addLayout(dropdowns_layout)

    def setup_parameters_line(self):
        parameters_layout = QHBoxLayout()
        self.entry_parameters = QLineEdit()
        self.entry_parameters.setMaxLength(11)
        parameters_layout.addWidget(QLabel("Parameters"))
        parameters_layout.addWidget(self.entry_parameters)
        self.main_layout.addLayout(parameters_layout)

    def setup_display_line(self):
        display_layout = QHBoxLayout()
        self.display_command = QLabel()
        self.display_command.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_command.setStyleSheet("""color: blue;
                                          font-family: Arial;
                                          font-size: 18px;
                                          padding: 8px;
                                          border-style: solid;
                                          border-width: 1px;
                                          border-color: black;""")
        display_layout.addWidget(self.display_command)
        self.main_layout.addLayout(display_layout)

    def setup_macro_display(self):
        self.macro_display_layout = QVBoxLayout()

        self.macro_sequence_display = QListWidget()
        self.macro_sequence_display.setDisabled(True)
        self.macro_sequence_display.itemSelectionChanged.connect(self.emit_item_selected)
        self.macro_display_layout.addWidget(self.macro_sequence_display)

        buttons_layout = QGridLayout()
        self.single_shot_btn = QPushButton("Single Shot")
        self.reset_btn = QPushButton("Reset Sequence")
        self.edit_btn = QPushButton("Select Step")
        self.clear_btn = QPushButton("Clear Command")

        buttons_layout.addWidget(self.single_shot_btn, 0, 0, 1, 2)
        self.single_shot_btn.clicked.connect(self.signal_distributor.SINGLE_SHOT_BUTTON_CLICKED)
        buttons_layout.addWidget(self.reset_btn, 0, 2, 1, 2)
        self.reset_btn.clicked.connect(self.reset_macro_fields_and_flags)
        buttons_layout.addWidget(self.edit_btn, 1, 0, 1, 2)
        self.edit_btn.clicked.connect(self.edit_macro_sequence)
        buttons_layout.addWidget(self.clear_btn, 1, 2, 1, 2)
        self.clear_btn.clicked.connect(self.clear_fields)

        self.macro_display_layout.addLayout(buttons_layout)
        self.main_layout.addLayout(self.macro_display_layout)

    @pyqtSlot()
    def select_next_macro_item(self):
        self.signal_distributor.DEBUG_MESSAGE.emit("selecting next macro item in CommandView")
        selected_items = self.macro_sequence_display.selectedItems()

        if selected_items:
            current_index = self.macro_sequence_display.row(selected_items[0])
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Current Index: {current_index}")
            next_index = current_index + 1
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Next Index: {next_index}")
            print(f"Macro Sequence Display Count: {self.macro_sequence_display.count()}")
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
    def edit_macro_sequence(self):
        self.is_editing = not self.is_editing
        self.macro_sequence_display.setDisabled(not self.is_editing)
        self.edit_btn.setText("Commit" if self.is_editing else "Select Step")

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
        self.signal_distributor.DEBUG_MESSAGE.emit("Fields have been cleared")

    @pyqtSlot()
    def reset_flags(self):
        # self.signal_distributor.state_changed.emit('waiting_for_completion', False, 'update')
        # self.signal_distributor.state_changed.emit('macro_running', False, 'update')
        # self.signal_distributor.state_changed.emit('response_received', False, 'update')
        # self.signal_distributor.state_changed.emit('completion_received', False, 'update')
        self.signal_distributor.DEBUG_MESSAGE.emit("Flags have NOT been reset")

    @pyqtSlot()
    def reset_macro_fields_and_flags(self):
        self.clear_fields()
        self.reset_flags()

    @pyqtSlot(str, str, str)
    def set_command_details(self, command, unit, parameters):
        self.set_command(command)
        self.set_unit_number(unit)
        self.set_parameters(parameters)
        self.set_code(command)

    @pyqtSlot()
    def send_current_item(self):
        selected_item = self.macro_sequence_display.currentItem()
        if selected_item:
            self.signal_distributor.CURRENT_ITEM_SIGNAL.emit(selected_item.text())
