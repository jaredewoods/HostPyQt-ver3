# custom_command_controller.py

class CustomCommandController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the view's checkbox toggled signals to the controller's method
        self.view.start_bit_checkbox.toggled.connect(self.update_model)
        self.view.checksum_checkbox.toggled.connect(self.update_model)
        self.view.carriage_return_checkbox.toggled.connect(self.update_model)

        # Connect the command line edit text change to update the checksum
        self.view.command_line_edit.textChanged.connect(self.handle_text_changed)

        # Initialize the view based on the model state
        self.update_view()

    def update_model(self):
        # Update the model based on the checkbox states
        self.model.set_start_bit_checked(self.view.start_bit_checkbox.isChecked())
        self.model.set_checksum_checked(self.view.checksum_checkbox.isChecked())
        self.model.set_carriage_return_checked(self.view.carriage_return_checkbox.isChecked())

        # Update the view based on the model state
        self.update_view()

    def update_view(self):
        # Update the view based on the model state
        self.update_start_bit()
        self.update_checksum()

    def update_start_bit(self):
        # Update the command text based on the start bit checkbox state
        command_text = self.view.command_line_edit.text()  # Do not remove \r since it's not in this field anymore
        if self.model.is_start_bit_checked():
            if not command_text.startswith("$"):
                command_text = "$" + command_text
        else:
            if command_text.startswith("$"):
                command_text = command_text[1:]
        self.set_command_text(command_text)

    def update_checksum(self):
        # Update the checksum based on the command text
        command_text = self.view.command_line_edit.text()  # Do not remove \r since it's not in this field anymore
        if self.model.is_checksum_checked():
            checksum = self.calculate_checksum(command_text)
            checksum_text = f"{checksum}\r"
            self.view.checksum_edit.setText(checksum_text)
        else:
            self.view.checksum_edit.clear()

    def handle_text_changed(self):
        # Update checksum on text change
        self.update_checksum()

    def set_command_text(self, text):
        # Temporarily disconnect the textChanged signal to prevent recursion
        self.view.command_line_edit.blockSignals(True)
        self.view.command_line_edit.setText(text)
        self.view.command_line_edit.blockSignals(False)

    def calculate_checksum(self, command_text):
        # Calculate the checksum excluding the first character if it is $
        if command_text.startswith("$"):
            command_text = command_text[1:]
        if not command_text:  # If command_text is empty, return '00'
            return "00"
        total_sum = sum(ord(char) for char in command_text)
        checksum = f"{total_sum:02X}"[-2:]  # Ensure the checksum is always two digits
        return checksum
