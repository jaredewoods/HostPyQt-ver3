from PyQt6.QtCore import QObject, pyqtSignal, QElapsedTimer


class MacroExecutor(QObject):
    def __init__(self, signal_distributor, flag_state_manager):
        super().__init__()
        print(f"Initializing MacroExecutor")
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        self.command_duration_stopwatch = QElapsedTimer()  # Initialize QElapsedTimer
        self.cycle_duration_stopwatch = QElapsedTimer()  # Initialize QElapsedTimer
        self.sequence_duration_stopwatch = QElapsedTimer()  # Initialize QElapsedTimer

        self._COMMANDS_COMPLETED = 0
        self._CYCLES_COMPLETED = 0
        self._SEQUENCES_COMPLETED = 0
        self._update_flag_statuses()
        print(f"MacroExecutor INITIALIZED")

        self.signal_distributor.macro_trigger_seq02.connect(self.seq02_waiting_for_completion)
        self.signal_distributor.macro_trigger_seq03.connect(self.seq03_handling_command_completion)

    def _update_flag_statuses(self):
        self._FLAGS = self.flag_state_manager.get_all_flag_statuses()
        self._SERIAL_CONNECTED = self._FLAGS.get("serial_connected")
        self._TCP_CONNECTED = self._FLAGS.get("tcp_connect")
        self._MACRO_READY_TO_RUN = self._FLAGS.get("macro_ready_to_run")
        self._MACRO_RUNNING = self._FLAGS.get("macro_running")
        self._MACRO_STOPPED = self._FLAGS.get("macro_stopped")
        self._MACRO_COMPLETED = self._FLAGS.get("macro_completed")
        self._WAITING_FOR_COMPLETION = self._FLAGS.get("waiting_for_completion")
        self._RESPONSE_RECEIVED = self._FLAGS.get("response_received")
        self._COMPLETION_RECEIVED = self._FLAGS.get("completion_received")
        self._ALARM_RECEIVED = self._FLAGS.get("alarm_received")
        self._DEBUG_MODE = self._FLAGS.get("debug_mode")
        self._DISPLAY_TIMESTAMP = self._FLAGS.get("display_timestamp")

    def execute_sequence(self):
        self._update_flag_statuses()
        print(f"Updated Flag statuses: {self._FLAGS}")
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            print(f"Executing Sequence")
            self.sequence_duration_stopwatch.start()
            self.seq00_initialize_cycle()
        else:
            print(f"Flag violation 00: {self._FLAGS}")

    def seq00_initialize_cycle(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):
            self.cycle_duration_stopwatch.start()
            self.seq01_send_command()

        else:
            print(f"Flag violation 01: {self._FLAGS}")

    def seq01_send_command(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):
            self.signal_distributor.send_command_signal.emit()
        else:
            print(f"Flag violation 02: {self._FLAGS}")

    def seq02_waiting_for_completion(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            self.command_duration_stopwatch.start()
        else:
            print(f"Flag violation 03: {self._FLAGS}")

    def seq03_handling_command_completion(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            command_time = self.command_duration_stopwatch.elapsed()  #
            self._COMMANDS_COMPLETED += 1
            # log cycle number, response values, elapsed time
            # run seq01 yo start the next line
            # else run seq04
            print(f"Command Completed in {command_time/1000} seconds\nCommands Completed: {self._COMMANDS_COMPLETED}")
        else:
            print(f"Flag violation 04: {self._FLAGS}")

    # this will need to be triggerd by an event
    def seq04_handling_cycle_completion(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            cycle_time = self.cycle_duration_stopwatch.elapsed()
            self._CYCLES_COMPLETED += 1
            print(f"Cycles Completed in {cycle_time/1000} seconds\nCycles Completed: {self._CYCLES_COMPLETED}")

            # compare completed cycles with total cycles
            # log starting next cycle
            # run seq01 to start the next cycles
            # else run seq05
        else:
            print(f"Flag violation 05: {self._FLAGS}")

    # this will need to be triggerd by an event
    def seq05_handling_sequence_completion(self):
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                self._MACRO_STOPPED and
                self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            sequence_time = self.sequences_duration_stopwatch.elapsed()
            self._SEQUENCES_COMPLETED += 1
            # log sequence completion
            # display statistics in UI popup
            # state changed macro_completed state changed True
            print(f"Sequence Completed in {sequence_time/1000} seconds\nSequences Completed: {self._SEQUENCES_COMPLETED}")
        else:
            print(f"Flag violation 06: {self._FLAGS}")
