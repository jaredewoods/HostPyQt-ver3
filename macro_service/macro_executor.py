from PyQt6.QtCore import QObject, pyqtSignal, QElapsedTimer, pyqtSlot, QTimer
from datetime import datetime

class MacroExecutor(QObject):

    def __init__(self, signal_distributor, flag_state_manager, max_retries=5):
        super().__init__()
        self.stop_time = None
        self.cycle_time = None
        self.start_time = None
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        self.command_duration_stopwatch = QElapsedTimer()

        self.cycle_duration_stopwatch = QElapsedTimer()
        self.sequence_duration_stopwatch = QElapsedTimer()
        self.max_retries = max_retries  # Set maximum retries
        self.retry_count = 0

        self._COMMANDS_COMPLETED = 0
        self._CYCLES_COMPLETED = 0
        self._SEQUENCES_COMPLETED = 0
        self._update_flag_statuses()
        self.signal_distributor.DEBUG_MESSAGE.emit(f"MacroExecutor INITIALIZED")

        self.response_timer = QTimer()
        self.completion_timeout_timer = QTimer()
        self.configure_timers()

    def configure_timers(self):
        self.response_timer.setInterval(500)
        self.completion_timeout_timer.setInterval(10000)
        self.response_timer.timeout.connect(self.handle_response_timeout)
        self.completion_timeout_timer.timeout.connect(self.handle_completion_timeout)

    def handle_failure(self, reason):
        self.response_timer.stop()
        self.completion_timeout_timer.stop()
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Operation failed after maximum retries: {reason}")
        self.signal_distributor.LOG_MESSAGE.emit(f"Operation failed after maximum retries: {reason}")

    def handle_response_timeout(self):
        # Handle response timeout logic
        self.retry_count += 1
        if self.retry_count <= self.max_retries:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Response timeout occurred, retrying {self.retry_count}/{self.max_retries}")
            self.response_timer.start()  # Retry logic, adjust as needed
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit("Response timeout occurred, maximum retries reached, giving up")
            self.handle_failure("Response timeout")

    @pyqtSlot()
    def handle_completion_timeout(self):
        # Handle completion timeout logic
        self.retry_count += 1
        if self.retry_count <= self.max_retries:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Completion timeout occurred, retrying {self.retry_count}/{self.max_retries}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Completion timeout occurred, retrying {self.retry_count}/{self.max_retries}")
            self.completion_timeout_timer.start()  # Retry logic, adjust as needed
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit("Completion timeout occurred, maximum retries reached, giving up")
            self.signal_distributor.LOG_MESSAGE.emit("Completion timeout occurred, maximum retries reached, giving up")
            self.handle_failure("Completion timeout")

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

    @pyqtSlot()
    def seq_start_sequence(self):
        self._update_flag_statuses()
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Updated Flag statuses: {self._FLAGS}")
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            self.signal_distributor.DEBUG_MESSAGE.emit(f"\nStarting Sequence")
            self.sequence_duration_stopwatch.start()
            self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
            self.start_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            # TODO: send a signal to status view to update the start time
            self.signal_distributor.LOG_MESSAGE.emit(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                                     f"  Sequence Started: {self.start_time}\n"
                                                     f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            self.seq00_start_cycle()
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation: {self._FLAGS}")

    @pyqtSlot()
    def seq00_start_cycle(self):
        self.signal_distributor.DEBUG_MESSAGE.emit("\n\nseq00_start_cycle")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):
            self.cycle_duration_stopwatch.start()
            self.signal_distributor.DEBUG_MESSAGE.emit(f"cycle_time: {self.cycle_duration_stopwatch.elapsed()}")
            self.seq01_start_command()

        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 00: {self._FLAGS}")

    @pyqtSlot()
    def seq01_start_command(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"\n\nseq01_start_command")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"cycle_time: {self.cycle_duration_stopwatch.elapsed()}")
        self.response_timer.start()
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):
            self.signal_distributor.CONSTRUCT_COMMAND_SIGNAL.emit()
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 01: {self._FLAGS}")

    @pyqtSlot()
    def seq02_waiting_for_completion(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"\n\nseq02_waiting_for_completion")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"cycle_time: {self.cycle_duration_stopwatch.elapsed()}")
        self.response_timer.stop()
        self.completion_timeout_timer.start()
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            self.command_duration_stopwatch.start()
            self.signal_distributor.DEBUG_MESSAGE.emit(f"command_time: {self.command_duration_stopwatch.elapsed()}")
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 02: {self._FLAGS}")

    @pyqtSlot()
    def seq03_handling_command_completion(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"\n\nseq03_handling_command_completion")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"cycle_time: {self.cycle_duration_stopwatch.elapsed()}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"command_time: {self.command_duration_stopwatch.elapsed()}")
        self.completion_timeout_timer.stop()
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            command_time = self.command_duration_stopwatch.elapsed()  #
            self._COMMANDS_COMPLETED += 1
            self.signal_distributor.DEBUG_MESSAGE.emit(
                f"Command Completed in {command_time / 1000} seconds\nCommands Completed: {self._COMMANDS_COMPLETED}")
            self.signal_distributor.NEXT_CYCLE_ITEM_SIGNAL.emit()
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 03: {self._FLAGS}")

    @pyqtSlot()
    def seq04_handling_cycle_completion(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"\n\nseq04_handling_cycle_completion")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"cycle_completed in: {self.cycle_duration_stopwatch.elapsed()}")
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                self._MACRO_RUNNING and
                not self._MACRO_STOPPED and
                not self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            self.cycle_time = self.cycle_duration_stopwatch.elapsed()
            sequence_time = self.sequence_duration_stopwatch.elapsed()
            self._CYCLES_COMPLETED += 1
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Cycle #{self._CYCLES_COMPLETED} completed in {self.cycle_time / 1000} seconds")
            self.signal_distributor.LOG_MESSAGE.emit(f'  completed: {self._CYCLES_COMPLETED}  |  cycle time: {self.cycle_time / 1000} s  |  total time: {sequence_time / 1000} s\n')
            self.signal_distributor.UPDATE_COMPLETED_CYCLES_SIGNAL.emit(self._CYCLES_COMPLETED)
            self.signal_distributor.REQUEST_TOTAL_CYCLES_SIGNAL.emit()
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 04: {self._FLAGS}")

    @pyqtSlot()
    def seq05_handling_sequence_completion(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"\n\nseq05_handling_sequence_completion")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"sequence_time: {self.sequence_duration_stopwatch.elapsed()}")
        self._update_flag_statuses()
        if (self._SERIAL_CONNECTED and
                not self._MACRO_RUNNING and
                self._MACRO_STOPPED and
                self._MACRO_COMPLETED and
                not self._WAITING_FOR_COMPLETION and
                not self._ALARM_RECEIVED):

            sequence_time = self.sequence_duration_stopwatch.elapsed()
            self._SEQUENCES_COMPLETED += 1
            self.stop_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            self.signal_distributor.DEBUG_MESSAGE.emit(
                f"Sequence Completed in {sequence_time / 1000} seconds\n"
                f"Sequences Completed: {self._SEQUENCES_COMPLETED}")
            self.signal_distributor.LOG_MESSAGE.emit(
                f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                f"  Completed Sequence: {self.stop_time}\n"
                f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                f"  Total Cycles: {self._CYCLES_COMPLETED}  |  Runtime: {sequence_time / 1000} seconds\n"
                f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n\n\n\n\n\n\n\n\n"
            )
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Flag violation 05: {self._FLAGS}")

    @pyqtSlot(int)
    def handle_total_cycles(self, total_cycles):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"{self._CYCLES_COMPLETED} of {total_cycles} completed in {self.cycle_time / 1000}s")
        if self._CYCLES_COMPLETED < total_cycles:
            self.signal_distributor.RESTART_CYCLE_SIGNAL.emit()
            self.signal_distributor.DEBUG_MESSAGE.emit("restart cycle")
        else:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_completed", True)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_stopped", True)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_running", False,)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_ready_to_run", False)
            self.seq05_handling_sequence_completion()
            self.signal_distributor.DEBUG_MESSAGE.emit("handling sequence completion")
