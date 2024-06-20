class MacroExecutor(QObject):
    log_message = pyqtSignal(str)  # Signal to emit log messages

    def __init__(self, model, view, command_view, serial_model, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.command_view = command_view
        self.serial_model = serial_model
        self.signal_distributor = signal_distributor

        self.current_command_index = 0
        self.current_cycle = 0
        self.total_cycles = 0
        self.running = False

    def start_macro(self):
        self.running = True
        self.total_cycles = int(self.view.macro_total_cycles_lbl.text())
        self.current_cycle = 0
        self.current_command_index = 0
        self.log_initialization()

    def log_initialization(self):
        self.log_message.emit(f"Macro starting for {self.total_cycles} cycles")
