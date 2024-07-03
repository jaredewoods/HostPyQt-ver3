import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import sys
import platform
import subprocess

class SystemCheck(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('System Check')
        self.geometry('740x480')

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill='both')

        self.system_info_tab = ttk.Frame(self.tab_control)
        self.check_results_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.system_info_tab, text='System Information')
        self.tab_control.add(self.check_results_tab, text='Check Results')

        self.system_info_layout = tk.Text(self.system_info_tab, wrap='word')
        self.system_info_layout.pack(expand=1, fill='both')

        self.check_results_layout = tk.Text(self.check_results_tab, wrap='word')
        self.check_results_layout.pack(expand=1, fill='both')

        self.task_step = 0
        self.results = []
        self.system_info = {}

        self.after(100, self.start_checks)

    def start_checks(self):
        self.load_config()
        self.after(100, self.run_checks_step)

    def load_config(self):
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        if 'Paths' not in self.config:
            messagebox.showerror('Error', 'Paths section is missing in config.ini')
            self.destroy()

    def run_checks_step(self):
        if self.task_step == 0:
            self.check_python_version()
        elif self.task_step == 1:
            self.check_paths()
        elif self.task_step == 2:
            self.check_required_libraries()
        elif self.task_step == 3 and platform.system() == 'Darwin':
            self.check_homebrew()
        elif self.task_step == 4:
            self.gather_system_info()
            self.display_results()
            self.display_system_info()
            return

        self.task_step += 1
        self.after(100, self.run_checks_step)

    def check_python_version(self):
        required_version = (3, 7)
        if sys.version_info < required_version:
            self.results.append((False, f"Python {required_version[0]}.{required_version[1]}+ is required."))
        else:
            self.results.append((True, f"Python version is {sys.version}."))

    def check_paths(self):
        paths_to_check = [
            self.config['Paths']['log_directory'],
            self.config['Paths']['macro_sequences_directory'],
            self.config['Paths']['command_dict'],
            self.config['Paths']['alarm_dict']
        ]
        for path in paths_to_check:
            full_path = os.path.abspath(path)
            if not os.path.exists(full_path):
                self.results.append((False, f"Path does not exist: {full_path}"))
            elif not os.access(full_path, os.R_OK | os.W_OK):
                self.results.append((False, f"Path is not readable/writable: {full_path}"))
            else:
                self.results.append((True, f"Path is accessible: {full_path}"))

    def check_required_libraries(self):
        required_libraries = ['tkinter', 'configparser']
        missing_libraries = []
        for lib in required_libraries:
            try:
                __import__(lib)
            except ImportError:
                missing_libraries.append(lib)
        if missing_libraries:
            self.results.append((False, f"Missing required libraries: {', '.join(missing_libraries)}"))
        else:
            self.results.append((True, "All required libraries are installed."))

    def check_homebrew(self):
        try:
            subprocess.run(['brew', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.results.append((True, "Homebrew is installed."))
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.results.append((False, "Homebrew is not installed."))

    def gather_system_info(self):
        self.system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version().replace("(", "\n("),
            "architecture": platform.machine(),
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
        }

    def display_system_info(self):
        self.system_info_layout.insert(tk.END, "System Information:\n")
        for key, value in self.system_info.items():
            self.system_info_layout.insert(tk.END, f"{key}: {value}\n")
        self.system_info_layout.config(state=tk.DISABLED)

    def display_results(self):
        self.check_results_layout.insert(tk.END, "Check Results:\n")
        all_checks_passed = True
        for success, message in self.results:
            status = "PASS" if success else "FAIL"
            if not success:
                all_checks_passed = False
            self.check_results_layout.insert(tk.END, f"{status}: {message}\n")
        self.check_results_layout.config(state=tk.DISABLED)

        if not all_checks_passed:
            messagebox.showerror("System Check Failed", "System checks failed. Please resolve the issues and restart the application.")
            self.destroy()

if __name__ == "__main__":
    app = SystemCheck()
    app.mainloop()
