# custom_command_controller.py

class CustomCommandController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # 1 Connect the view's checkbox toggled signal to the controller's method
        self.view.start_bit_checkbox.toggled.connect(self.update_model)

        # UV Initialize the view based on the model state
        self.update_view()

    def update_model(self):
        # 2 Update the model based on the checkbox state
        self.model.set_start_bit_checked(self.view.start_bit_checkbox.isChecked())
        # UV Update the view based on the model state
        self.update_view()

    def update_view(self):
        # UV Update the view based on the model state
        if self.model.is_start_bit_checked():
            if not self.view.command_line_edit.text().startswith("$"):
                self.view.command_line_edit.setText("$" + self.view.command_line_edit.text())
        else:
            if self.view.command_line_edit.text().startswith("$"):
                self.view.command_line_edit.setText(self.view.command_line_edit.text()[1:])
