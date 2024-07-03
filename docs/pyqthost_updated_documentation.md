
# PyQtHost Project Class and Sequence Diagrams with Dependencies

## High-Level Component Diagram
```
[MainWindow]
  |
  +-- [CommandView]
  |
  +-- [SerialTab]
  |
  +-- [TcpTab]
  |
  +-- [MacroTab]
  |
  +-- [StatusView]
```

## Detailed Module Breakdown with Dependencies

### CommandService

**Class Diagram:**
```
[CommandService]
  - Attributes and methods to be defined based on your code
```

### CommandController

**Class Diagram:**
```
[CommandController]
  - __init__(model, view)
  - update_model()
  - update_view()
  - set_command_text(text)
  - handle_text_changed()
```

**Sequence Diagram for handle_text_changed():**
```
User -> CommandController: handle_text_changed()
CommandController -> CommandModel: update_model()
CommandModel -> CommandView: update_view()
```

**Sequence Diagram for set_command_text():**
```
User -> CommandController: set_command_text()
CommandController -> CommandModel: set_command_code()
CommandModel -> CommandController: Return updated model
CommandController -> CommandView: update_view()
```

**Sequence Diagram for update_model():**
```
User -> CommandController: update_model()
CommandController -> CommandModel: set_start_bit_checked()
CommandController -> CommandModel: set_checksum_checked()
CommandController -> CommandModel: set_carriage_return_checked()
CommandController -> CommandModel: set_unit_no()
CommandController -> CommandModel: set_command_code()
CommandController -> CommandModel: set_parameters()
CommandController -> CommandView: update_view()
```

### CommandModel

**Class Diagram:**
```
[CommandModel]
  - __init__()
  - construct_command()
  - calculate_checksum(command)
  - set_start_bit_checked(value)
  - set_unit_no(value)
  - set_command_code(value)
  - set_parameters(value)
  - set_checksum_checked(value)
  - set_carriage_return_checked(value)
```

**Sequence Diagram for construct_command():**
```
CommandController -> CommandModel: construct_command()
CommandModel -> Self: calculate_checksum(command)
CommandModel -> Self: set_command_code(value)
CommandModel -> Self: set_parameters(value)
CommandModel -> CommandController: Return constructed command
```

### CommandView

**Class Diagram:**
```
[CommandView]
  - __init__(btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name)
  - setup_preset_buttons(btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name)
  - setup_checkboxes()
  - setup_dropdowns_and_parameters()
  - setup_parameters_line()
  - setup_display_line()
  - setup_macro_display()
  - emit_item_selected()
  - update_macro_sequence(sequence)
  - edit_macro_sequence()
  - set_command(command)
  - set_unit_number(unit_number)
  - set_parameters(parameters)
  - set_code(code)
  - clear_fields()
```

**Sequence Diagram for set_command():**
```
CommandController -> CommandView: set_command()
CommandView -> CommandModel: set_command_code()
CommandView -> CommandModel: set_parameters()
CommandView -> CommandController: Return updated view
```

**Sequence Diagram for update_macro_sequence():**
```
CommandController -> CommandView: update_macro_sequence(sequence)
CommandView -> Self: clear()
CommandView -> Self: addItem(QListWidgetItem(item))
```

### MacroController

**Class Diagram:**
```
[MacroController]
  - __init__(model, view, command_view, signal_distributor, flag_state_manager)
  - get_macro_directory()
  - populate_macro_combobox()
  - on_macro_dropdown_activated(index)
  - update_macro_ready_state()
  - handle_macro_file_selection(selected_file)
  - read_macro_file(file_path)
  - parse_macro_file_content(lines)
  - update_ui_with_macro_data(suggested_cycles, macro_commands)
  - load_macro_file(file_name)
  - load_macro_sequence_line()
  - load_command_into_view(command, unit, parameters)

```

**Sequence Diagram for load_macro_file():**
```
User -> MacroController: load_macro_file(file_name)
MacroController -> Self: get_macro_directory()
MacroController -> Self: read_macro_file(file_path)
MacroController -> Self: parse_macro_file_content(lines)
MacroController -> Self: update_ui_with_macro_data(suggested_cycles, macro_commands)
MacroController -> Self: Return suggested_cycles, macro_commands

```

### MacroModel

**Class Diagram:**
```
[MacroModel]
  - __init__()
  - load_macro_file(macro_sequence_file_path)
  - get_recommended_cycles()
  - _parse_macro_commands(lines)
  - get_macro_filenames(directory)

```

**Sequence Diagram for load_macro_file():**
```
MacroController -> MacroModel: load_macro_file(macro_sequence_file_path)
MacroModel -> Self: read file lines
MacroModel -> Self: _parse_macro_commands(lines)
MacroModel -> MacroController: Return parsed commands

```

### MacroView

**Class Diagram:**
```
[MacroView]
  - __init__()
  - populate_macro_select_combo(macro_files)
  - update_total_cycles(cycles)

```

**Sequence Diagram for populate_macro_select_combo():**
```
MacroController -> MacroView: populate_macro_select_combo(macro_files)
MacroView -> Self: clear()
MacroView -> Self: addItem("")
MacroView -> Self: addItems(macro_files)

```

### SerialController

**Class Diagram:**
```
[SerialController]
  - __init__(model, view, signal_distributor)
  - _populate_ports()
  - connect_serial()
  - disconnect_serial()
  - _update_connection_state(connected)

```

**Sequence Diagram for connect_serial():**
```
User -> SerialController: connect_serial()
SerialController -> SerialModel: connect(port, baudrate)
SerialModel -> SerialController: Return success/failure
alt success
    SerialController -> Self: _update_connection_state(True)
    SerialController -> SignalDistributor: emit('serial_connected', True, 'validate')
    SerialController -> Self: debug_message.emit("Connected to {port} at {baudrate} baudrate")
else failure
    SerialController -> Self: _update_connection_state(False)
    SerialController -> SignalDistributor: emit('serial_connected', False, 'validate')
    SerialController -> Self: debug_message.emit("Failed to connect to {port}")

```

### SerialModel

**Class Diagram:**
```
[SerialModel]
  - __init__()
  - get_available_ports()
  - connect(port, baudrate=9600)
  - disconnect_serial()

```

**Sequence Diagram for connect():**
```
SerialController -> SerialModel: connect(port, baudrate)
SerialModel -> Self: serial.Serial(port, baudrate)
alt success
    SerialModel -> SerialController: Return True
else failure
    SerialModel -> SerialController: Return False

```

### SerialView

**Class Diagram:**
```
[SerialView]
  - __init__()
  - _check_selections()
  - set_ports(ports)

```

**Sequence Diagram for _check_selections():**
```
User -> SerialView: _check_selections()
alt selections valid
    SerialView -> Self: setEnabled(True)
else selections invalid
    SerialView -> Self: setEnabled(False)

```


**Sequence Diagram for set_ports():**
```
SerialController -> SerialView: set_ports()
SerialView -> SerialModel: get_available_ports()
SerialModel -> SerialView: Return available ports
SerialView -> Self: Update ports in view
```

### TCPController

**Class Diagram:**
```
[TCPController]
  - __init__(model, view, signal_distributor)
  - connect_tcp()
  - disconnect_tcp()
  - _update_connection_btn_state(connected)

```

**Sequence Diagram for connect_tcp():**
```
User -> TCPController: connect_tcp()
TCPController -> TCPModel: connect(ip_address, port)
TCPModel -> TCPController: Return success/failure
alt success
    TCPController -> SignalDistributor: emit('tcp_connected', True, 'validate')
    TCPController -> Self: debug_message.emit("Connected to {ip_address}:{port}")
else failure
    TCPController -> SignalDistributor: emit('tcp_connected', False, 'update')
    TCPController -> Self: debug_message.emit("Failed to connect to {ip_address}:{port}")

```

### TCPModel

**Class Diagram:**
```
[TCPModel]
  - __init__()
  - connect(ip_address, port)
  - disconnect()

```

**Sequence Diagram for connect():**
```
TCPController -> TCPModel: connect(ip_address, port)
TCPModel -> Self: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPModel -> Self: tcp_socket.connect((ip_address, int(port)))
alt success
    TCPModel -> TCPController: Return True
else failure
    TCPModel -> TCPController: Return False

```

### TCPView

**Class Diagram:**
```
[TCPView]
  - __init__()
  - _check_selections()

```

**Sequence Diagram for _check_selections():**
```
User -> TCPView: _check_selections()
alt selections valid
    TCPView -> Self: setEnabled(True)
else selections invalid
    TCPView -> Self: setEnabled(False)

```

### FlagStateManager

**Class Diagram:**
```
[FlagStateManager]
  - __init__(signal_distributor)
  - update_state(flag_name, value, condition)
  - get_flag_status(flag_name)

```

**Sequence Diagram for update_state():**
```
SignalDistributor -> FlagStateManager: update_state(flag_name, value, condition)
alt update
    FlagStateManager -> Self: setattr(flag_name, value)
elif validate
    FlagStateManager -> Self: if current_value != value: setattr(flag_name, value)
elif toggle
    FlagStateManager -> Self: setattr(flag_name, not current_value)
FlagStateManager -> Self: emit state_updated(flag_name, value)

```

### FlagStateView

**Class Diagram:**
```
[FlagStateView]
  - __init__(flag_state_manager)
  - populate_table()
  - update_table(flag_name, value, update_condition)

```

**Sequence Diagram for update_table():**
```
FlagStateManager -> FlagStateView: update_table()
FlagStateView -> Self: Update UI table with new state
```

### MainWindow

**Class Diagram:**
```
[MainWindow]
  - __init__()
  - on_state_changed(flag_name, value, update_condition)
  - handle_serial_connected(value)
  - handle_tcp_connected(value)
  - handle_macro_ready_to_run(value)
  - handle_macro_running(value)
  - handle_macro_stopped(value)
  - handle_macro_completed(value)
  - handle_waiting_for_response(value)
  - handle_response_received(value)
  - handle_completion_received(value)
  - handle_alarm_received(value)
  - handle_debug_mode(value)
  - handle_display_timestamp(value)
  - update_log_display(message)
```

**Sequence Diagram for handle_macro_running():**
```
FlagStateManager -> MainWindow: on_state_changed(flag_name, value, update_condition)
MainWindow -> LogDisplay: append(f"State changed: {flag_name} -> {value}")
alt handler exists
    MainWindow -> Self: handler(value)

```

### SignalDistributor

**Class Diagram:**
```
[SignalDistributor]
  - __init__()
  - emit_state_change(flag_name, value, update_condition)

```

**Sequence Diagram for emit_state_change():**
```
AnyComponent -> SignalDistributor: emit_state_change(flag_name, value, update_condition)
SignalDistributor -> Self: emit(state_changed(flag_name, value, update_condition))

```

### StatusView

**Class Diagram:**
```
[StatusView]
  - __init__()
  - create_status_time_layout()
  - create_status_connection_layout()
  - update_label_color(label, value)
  - update_serial_status(value)
  - update_tcp_status(value)
  - update_macro_status(value)

```

**Sequence Diagram for update_macro_status():**
```
AnyComponent -> StatusView: update_serial_status(value)
StatusView -> Self: update_label_color(self.serial_status_label, value)

```
