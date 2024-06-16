from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QComboBox, QLineEdit, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from resources.command_dictionary import commands

class CommandView(QWidget):
    def __init__(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        super().__init__()

        self.main_layout = QVBoxLayout()

        # Initialize UI components
        self.setup_checkboxes()
        self.setup_dropdowns_and_parameters()
        self.setup_display_line()
        self.setup_control_buttons_layout()
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
        self.display_command.setStyleSheet("""color: white;
                                          font-family: Arial;
                                          font-size: 18px;
                                          padding: 8px;
                                          border-style: solid;
                                          border-width: 1px;
                                          border-color: black;""")
        display_layout.addWidget(self.display_command)
        self.main_layout.addLayout(display_layout)

    def setup_control_buttons_layout(self):
        buttons_layout = QHBoxLayout()

        self.send_btn = QPushButton("Send")
        self.clear_btn = QPushButton("Clear")
        buttons_layout.addWidget(self.send_btn)
        buttons_layout.addWidget(self.clear_btn)

        self.main_layout.addLayout(buttons_layout)

    def setup_macro_display(self):
        self.macro_display_layout = QVBoxLayout()

        self.macro_sequence_display = QTextEdit("no macro loaded")
        self.macro_sequence_display.setReadOnly(False)
        self.macro_display_layout.addWidget(self.macro_sequence_display)

        buttons_layout = QGridLayout()
        self.send_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.clear_btn = QPushButton("Clear")
        self.reset_btn = QPushButton("Reset")
        buttons_layout.addWidget(self.send_btn, 0, 0, 1, 2)
        buttons_layout.addWidget(self.stop_btn, 0, 2, 1, 2)
        buttons_layout.addWidget(self.clear_btn, 1, 0, 1, 2)
        buttons_layout.addWidget(self.reset_btn, 1, 2, 1, 2)
        self.macro_display_layout.addLayout(buttons_layout)

        self.main_layout.addLayout(self.macro_display_layout)

    def update_macro_sequence(self, sequence):
        self.macro_sequence_display.setPlainText(sequence)

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
