from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QComboBox, QLineEdit, QLabel, QPushButton, QListWidgetItem
from PyQt6.QtCore import Qt
from resources.command_dictionary import commands

class CommandView(QWidget):
    itemSelected = pyqtSignal()  # Signal to emit when an item is selected
    single_shot_btn_clicked = pyqtSignal()
    reset_btn_clicked = pyqtSignal()
    debug_message = pyqtSignal()
    run_next_command = pyqtSignal()
    signal_cycle_completed = pyqtSignal()

    def __init__(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.is_editing = False  # Track the editing state

        # Initialize UI components
        self.setup_dropdowns_and_parameters()
        self.setup_checkboxes()
        self.setup_display_line()
        self.setup_macro_display()

        self.setLayout(self.main_layout)

    def setup_preset_buttons(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        # Preset buttons
        preset_layout = QGridLayout()
        self.btn_preset1 = QPushButton(btn_preset1_name)
        self.btn_preset1.setEnabled(False)
        preset_layout.addWidget(self.btn_preset1, 0, 0, 1, 2)
        self.btn_preset2 = QPushButton(btn_preset2_name)
        self.btn_preset2.setEnabled(False)
        preset_layout.addWidget(self.btn_preset2, 0, 2, 1, 2)
        self.btn_preset3 = QPushButton(btn_preset3_name)
        self.btn_preset3.setEnabled(False)
        preset_layout.addWidget(self.btn_preset3, 1, 0, 1, 2)
        self.btn_preset4 = QPushButton(btn_preset4_name)
        self.btn_preset4.setEnabled(False)
        preset_layout.addWidget(self.btn_preset4, 1, 2, 1, 2)
        self.main_layout.addLayout(preset_layout)

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
        dropdowns_layout.addWidget(QLabel("UNo"))
        dropdowns_layout.addWidget(self.dropdown_unit_no)
        dropdowns_layout.addWidget(QLabel("CMND"))

        self.dropdown_code.addItem("")
        for command in commands.keys():
            self.dropdown_code.addItem(command)

        dropdowns_layout.addWidget(self.dropdown_code)

        self.entry_parameters = QLineEdit()
        self.entry_parameters.setFixedWidth(90)
        dropdowns_layout.addWidget(QLabel("PRM"))
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
        self.macro_sequence_display.setDisabled(True)  #
        self.macro_sequence_display.itemSelectionChanged.connect(self.emit_item_selected)  # Connect the selection change event
        self.macro_display_layout.addWidget(self.macro_sequence_display)

        buttons_layout = QGridLayout()
        self.single_shot_btn = QPushButton("Single Shot")
        self.reset_btn = QPushButton("Reset Sequence")
        self.edit_btn = QPushButton("Select Step")
        self.clear_btn = QPushButton("Clear Command")

        buttons_layout.addWidget(self.single_shot_btn, 0, 0, 1, 2)
        self.single_shot_btn.clicked.connect(self.on_single_shot_btn_clicked)
        buttons_layout.addWidget(self.reset_btn, 0, 2, 1, 2)
        self.reset_btn.clicked.connect(self.reset_macro)
        buttons_layout.addWidget(self.edit_btn, 1, 0, 1, 2)
        self.edit_btn.clicked.connect(self.edit_macro_sequence)
        buttons_layout.addWidget(self.clear_btn, 1, 2, 1, 2)
        self.clear_btn.clicked.connect(self.clear_fields)

        self.macro_display_layout.addLayout(buttons_layout)
        self.main_layout.addLayout(self.macro_display_layout)

    def select_next_macro_item(self):
        print("selecting next macro item in CommandView")
        selected_items = self.macro_sequence_display.selectedItems()

        if selected_items:
            current_index = self.macro_sequence_display.row(selected_items[0])
            print(f"Current Index: {current_index}")
            next_index = current_index + 1
            print(f"Next Index: {next_index}")
            print(f"Macro Sequence Display Count: {self.macro_sequence_display.count()}")
            if next_index < self.macro_sequence_display.count():
                self.macro_sequence_display.setCurrentRow(next_index)
                self.run_next_command.emit()
            else:
                self.signal_cycle_completed.emit()

    def restart_cycle(self):
        self.macro_sequence_display.setCurrentRow(0)
        self.run_next_command.emit()

    def on_single_shot_btn_clicked(self):
        self.single_shot_btn_clicked.emit()

    def emit_item_selected(self):
        self.itemSelected.emit()

    def update_macro_sequence(self, sequence):
        self.macro_sequence_display.clear()
        for item in sequence.split('\n'):
            self.macro_sequence_display.addItem(QListWidgetItem(item))

    def edit_macro_sequence(self):
        self.is_editing = not self.is_editing
        self.macro_sequence_display.setDisabled(not self.is_editing)
        self.edit_btn.setText("Commit" if self.is_editing else "Select Step")

    def set_command(self, command):
        print(f"Command set: {command}")  # Debug statement
        self.display_command.setText(command)

    def set_unit_number(self, unit_number):
        print(f"Unit number set: {unit_number}")  # Debug statement
        index = self.dropdown_unit_no.findText(str(unit_number))
        if index != -1:
            self.dropdown_unit_no.setCurrentIndex(index)

    def set_parameters(self, parameters):
        print(f"Parameters set: {parameters}")  # Debug statement
        self.entry_parameters.setText(parameters)

    def set_code(self, code):
        print(f"Code set: {code}")  # Debug statement
        index = self.dropdown_code.findText(code)
        if index != -1:
            self.dropdown_code.setCurrentIndex(index)
        else:
            self.dropdown_code.setCurrentText(code)

    def clear_fields(self):
        self.set_unit_number("")
        self.set_code("")
        self.set_parameters("")
        # self.debug_message.emit("Fields have been cleared")

    def reset_flags(self):
        print("command view needs signal_distributor")
        # self.signal_distributor.state_changed.emit('waiting_for_completion', False, 'update')
        # self.signal_distributor.state_changed.emit('macro_running', False, 'update')
        # self.signal_distributor.state_changed.emit('response_received', False, 'update')
        # self.signal_distributor.state_changed.emit('completion_received', False, 'update')
        # self.debug_message.emit("Flags have been reset")

    def reset_macro(self):
        self.clear_fields()
        self.reset_flags()
