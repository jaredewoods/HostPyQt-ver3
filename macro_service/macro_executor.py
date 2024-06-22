from PyQt6.QtCore import QObject, pyqtSignal


class MacroExecutor(QObject):

    def __init__(self, signal_distributor, flag_state_manager):
        super().__init__()
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        self.cycles_completed = 0
        print(f"Current Cycle = {self.cycles_completed}")

    # uncertain if I need the individual flag
    def execute_sequence(self):
        print(f"Shout out from Macro executor")
        self.seq00_initialize()

    def seq00_initialize(self):
        # there has to be a better way to give veeveryone access to all the flags
        flags = self.flag_state_manager.get_all_flag_statuses()
        print(f"Flag statuses: {flags}")
        self.seq01_send_command()

    def seq01_send_command(self):
        self.signal_distributor.send_command_signal.emit()
        self.seq02_waiting_for_completion()

    def seq02_waiting_for_completion(self):
        # advance sequence line to load the next command
        # start elapsed timer
        self.seq03_handling_command_completion()

    def seq03_handling_command_completion(self):
        # parse response values
        # stop elapsed timer
        # log cycle number, response values, elapsed time
        # run seq01 yo start the next line
        # else run seq04
        self.seq04_handling_cycle_completion()

    def seq04_handling_cycle_completion(self):
        # compare completed cycles with total cycles
        # add one and log cycle completed
        # log starting next cycle
        # run seq01 to start the next cycles
        # else run seq05
        self.seq05_handling_sequence_completion()

    def seq05_handling_sequence_completion(self):
        # log sequence completion
        # display statistics in UI popup
        # state changed macro_completed state changed True
        pass
