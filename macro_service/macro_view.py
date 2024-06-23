# macro_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit

class MacroView(QWidget):
    """
    MacroView Class

    This class represents a view for macro sequence selection and control.

    Constructor:
        MacroView()

    Methods:
        - populate_macro_select_combo(macro_files)
            - Populates the macro sequence selection combobox with the given macro files.
            - Parameters:
                - macro_files: List[str] - A list of macro file names.
            - Returns: None

        - update_total_cycles(cycles)
            - Updates the total cycles label with the given cycles value.
            - Parameters:
                - cycles: int - The total number of cycles.
            - Returns: None
    """
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # Macro Sequence Selection
        layout.addWidget(QLabel("Macro Sequence"), 0, 0, 1, 2)
        self.macro_select_cbx = QComboBox()
        layout.addWidget(self.macro_select_cbx, 1, 0, 1, 2)

        # Cycle Count Entry
        layout.addWidget(QLabel("Total"), 0, 2, 1, 1)
        self.macro_total_cycles_lbl = QLineEdit("")
        layout.addWidget(self.macro_total_cycles_lbl, 1, 2, 1, 1)

        # Cycle Completed Entry
        layout.addWidget(QLabel("Cycle"), 0, 3, 1, 1)
        self.macro_completed_cycles_lbl = QLineEdit("")
        layout.addWidget(self.macro_completed_cycles_lbl, 1, 3, 1, 1)

        # Macro Start Button
        self.macro_start_btn = QPushButton("Start")
        self.macro_start_btn.setEnabled(False)
        layout.addWidget(self.macro_start_btn, 2, 0, 1, 2)

        # Macro Stop Button
        self.macro_stop_btn = QPushButton("Stop")
        self.macro_stop_btn.setEnabled(False)
        layout.addWidget(self.macro_stop_btn, 2, 2, 1, 2)

        # Adjust column stretch to balance the layout
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)

    def populate_macro_select_combo(self, macro_files):
        self.macro_select_cbx.clear()
        self.macro_select_cbx.addItem("")
        self.macro_select_cbx.addItems(macro_files)

    def update_total_cycles(self, cycles):
        self.macro_total_cycles_lbl.setText(str(cycles))

    def update_completed_cycles(self, cycles):
        self.macro_completed_cycles_lbl.setText(str(cycles))
        print(f"updating completed cycles {cycles}")
