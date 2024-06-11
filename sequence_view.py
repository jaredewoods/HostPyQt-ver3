from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class SequenceView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.sequence_display = QTextEdit()
        self.sequence_display.setReadOnly(True)
        layout.addWidget(self.sequence_display)
        self.setLayout(layout)
