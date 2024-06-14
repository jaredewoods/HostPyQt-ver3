# command_compiler_model.py

class CommandCompilerModel:
    def __init__(self):
        self.start_bit_checked = True
        self.unit_no = ""
        self.command_code = ""
        self.parameters = ""
        self.checksum_checked = True
        self.carriage_return_checked = True

    def construct_command(self):
        command = ""
        if self.start_bit_checked:
            command += "$"
        command += self.unit_no
        command += self.command_code
        command += self.parameters
        if self.checksum_checked:
            checksum = self.calculate_checksum(command)
            command += checksum
        if self.carriage_return_checked:
            command += "\r"
        return command

    @staticmethod
    def calculate_checksum(command):
        if command.startswith("$"):
            command = command[1:]
        if not command:
            return "00"
        total_sum = sum(ord(char) for char in command)
        checksum = f"{total_sum:02X}"[-2:]  # Ensure the checksum is always two digits
        return checksum

    def set_start_bit_checked(self, value):
        self.start_bit_checked = value

    def set_unit_no(self, value):
        self.unit_no = value

    def set_command_code(self, value):
        self.command_code = value.upper()  # Ensure uppercase

    def set_parameters(self, value):
        self.parameters = value.upper()  # Ensure uppercase

    def set_checksum_checked(self, value):
        self.checksum_checked = value

    def set_carriage_return_checked(self, value):
        self.carriage_return_checked = value