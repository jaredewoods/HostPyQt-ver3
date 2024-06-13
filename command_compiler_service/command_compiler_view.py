from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QComboBox, QLineEdit, QLabel, QPushButton, QTextEdit
from resources.command_dictionary import commands

class CommandCompilerView(QWidget):
    def __init__(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        super().__init__()

        self.main_layout = QVBoxLayout()

        # Initialize UI components
        # self.setup_preset_buttons(btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name)
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
        self.dropdown_unit_no.addItems(["1", "2"])
        self.dropdown_code = QComboBox()
        self.dropdown_code.setEditable(True)
        dropdowns_layout.addWidget(QLabel("UnitNo"))
        dropdowns_layout.addWidget(self.dropdown_unit_no)
        dropdowns_layout.addWidget(QLabel("Cmnd"))

        # Load commands into the dropdown
        for command in commands.keys():
            self.dropdown_code.addItem(command)

        dropdowns_layout.addWidget(self.dropdown_code)

        self.entry_parameters = QLineEdit()
        self.entry_parameters.setFixedWidth(90)
        dropdowns_layout.addWidget(QLabel("Prm"))
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
        display_layout.addWidget(QLabel("Command:"))
        display_layout.addWidget(self.display_command)
        self.main_layout.addLayout(display_layout)

    def setup_control_buttons_layout(self):
        buttons_layout = QGridLayout()
        self.button_start = QPushButton("Start")
        self.button_stop = QPushButton("Stop")
        self.button_clear = QPushButton("Clear")
        self.button_reset = QPushButton("Reset")
        buttons_layout.addWidget(self.button_start, 0, 0, 1, 2)
        buttons_layout.addWidget(self.button_stop, 0, 2, 1, 2)
        buttons_layout.addWidget(self.button_clear, 1, 0, 1, 2)
        buttons_layout.addWidget(self.button_reset, 1, 2, 1, 2)
        self.main_layout.addLayout(buttons_layout)

    def setup_macro_display(self):
        macro_display_layout = QVBoxLayout()
        self.macro_sequence_display = QTextEdit()
        self.macro_sequence_display.setReadOnly(True)
        macro_display_layout.addWidget(QLabel("Macro Sequence"))
        macro_display_layout.addWidget(self.macro_sequence_display)
        self.main_layout.addLayout(macro_display_layout)
