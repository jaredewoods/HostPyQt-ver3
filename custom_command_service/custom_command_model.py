# custom_command_model.py

class CustomCommandModel:
    def __init__(self):
        self._start_bit_checked = True
        self._checksum_checked = True
        self._carriage_return_checked = True

    def set_start_bit_checked(self, value):
        self._start_bit_checked = value

    def is_start_bit_checked(self):
        return self._start_bit_checked

    def set_checksum_checked(self, value):
        self._checksum_checked = value

    def is_checksum_checked(self):
        return self._checksum_checked

    def set_carriage_return_checked(self, value):
        self._carriage_return_checked = value

    def is_carriage_return_checked(self):
        return self._carriage_return_checked
