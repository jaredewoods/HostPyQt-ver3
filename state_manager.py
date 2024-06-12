# state_manager.py
"""Define the state flags.
Implement the slot to update the state based on the signal."""

class StateManager:

    def __init__(self):
        self.serial_ready_to_connect = False  # Indicates if the serial port and baud rate are selected, and the serial connection is ready to be established.
        self.serial_connected = False         # Indicates if the serial port is currently connected.
        self.tcp_ready_to_connect = False     # Indicates if the TCP/IP address and port are selected, and the TCP/IP connection is ready to be established.
        self.tcp_connected = False            # Indicates if the TCP/IP connection is currently established.
        self.macro_ready_to_run = False       # Indicates if both the serial and TCP connections are established, a sequence is selected, and a valid number is set for the total cycles, making the macro ready to run.
        self.macro_running = False            # Indicates if a macro is currently running.
        self.macro_stopped = False            # Indicates if a macro execution is stopped.
        self.macro_completed = False          # Indicates if a macro has completed its execution.
        self.waiting_for_response = False     # Indicates if the system is waiting for a response after sending a command.
        self.response_received = False        # Indicates if a response has been received for a command.
        self.completion_received = False      # Indicates if a completion signal has been received after a command.
        self.alarm_received = False           # Indicates if an alarm signal has been received.
        self.debug_mode = False               # Indicates if the system is currently in debug mode.
        self.display_timestamp = False        # Indicates if timestamps should be displayed in the log display; timestamps are always logged regardless.

    @pyqtSlot(str, bool, str)
    def update_state(self, flag_name, value, update_condition):
        if not hasattr(self, flag_name):
            print(f"Unknown flag: {flag_name}")
            return

        current_value = getattr(self, flag_name)

        if update_condition == 'update':
            setattr(self, flag_name, value)
        elif update_condition == 'conditional_update' and current_value != value:
            setattr(self, flag_name, value)
        elif update_condition == 'toggle':
            setattr(self, flag_name, not current_value)

        print(f"Updated {flag_name} to {getattr(self, flag_name)}")