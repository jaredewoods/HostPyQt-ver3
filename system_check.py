import os
import sys
import platform
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SystemCheck(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_results_tab = None
        self.system_info_tab = None
        self.check_results_layout = None
        self.system_info_layout = None
        self.tabs = None
        self.layout = None
        self.central_widget = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('System Check')
        self.setGeometry(300, 300, 740, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.system_info_tab = QWidget()
        self.check_results_tab = QWidget()

        self.tabs.addTab(self.system_info_tab, "System Information")
        self.tabs.addTab(self.check_results_tab, "Check Results")

        self.system_info_layout = QVBoxLayout()
        self.system_info_tab.setLayout(self.system_info_layout)

        self.check_results_layout = QVBoxLayout()
        self.check_results_tab.setLayout(self.check_results_layout)

    @staticmethod
    def add_info(text, tab, status=None):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(10)
        label.setFont(font)
        label.setContentsMargins(10, 2, 10, 2)  # Adjust margins to control spacing

        if status == "FAIL":
            label.setStyleSheet("color: red;")

        tab.addWidget(label)

    @staticmethod
    def check_python_version():
        required_version = (3, 7)
        if sys.version_info < required_version:
            return False, f"Python {required_version[0]}.{required_version[1]}+ is required."
        return True, f"Python version is {sys.version}."

    @staticmethod
    def check_path_accessibility(path):
        full_path = os.path.abspath(path)
        print(f"Checking path: {full_path}")  # Debug statement
        if not os.path.exists(full_path):
            return False, f"Path does not exist: {full_path}"
        if not os.access(full_path, os.R_OK | os.W_OK):
            return False, f"Path is not readable/writable: {full_path}"
        return True, f"Path is accessible: {full_path}"

    @staticmethod
    def check_required_libraries():
        required_libraries = ['PyQt6', 'serial']
        missing_libraries = []
        for lib in required_libraries:
            try:
                __import__(lib)
            except ImportError:
                missing_libraries.append(lib)
        if missing_libraries:
            return False, f"Missing required libraries: {', '.join(missing_libraries)}"
        return True, "All required libraries are installed."

    @staticmethod
    def check_homebrew():
        try:
            subprocess.run(['brew', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, "Homebrew is installed."
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "Homebrew is not installed."

    @staticmethod
    def gather_system_info():
        info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version().replace("(", "\n("),
            "architecture": platform.machine(),
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
        }
        return info

    def run_checks(self):
        results = []

        # Check Python version
        result = self.check_python_version()
        results.append(result)

        # Define and check paths relative to the project root
        project_root = os.path.dirname(os.path.abspath(__file__))
        paths_to_check = [
            os.path.join(project_root, 'logs'),
            os.path.join(project_root, 'macro_sequences'),
            os.path.join(project_root, 'src', 'resources', 'command_dict.py'),
            os.path.join(project_root, 'src', 'resources', 'alarm_dict.py')
        ]
        for path in paths_to_check:
            results.append(self.check_path_accessibility(path))

        # Check required libraries
        libraries_status, libraries_message = self.check_required_libraries()
        results.append((libraries_status, libraries_message))

        # Check Homebrew (macOS specific)
        if platform.system() == 'Darwin':
            results.append(self.check_homebrew())

        # Gather system info
        system_info = self.gather_system_info()

        # Display results
        self.add_info("System Information:", self.system_info_layout)
        for key, value in system_info.items():
            self.add_info(f"{key}: {value}", self.system_info_layout)

        # Display required libraries
        self.add_info("\nRequired Libraries:", self.system_info_layout)
        for lib in ['PyQt6', 'serial']:
            self.add_info(f"Library: {lib}", self.system_info_layout)

        self.add_info("\nCheck Results:", self.check_results_layout)
        for success, message in results:
            status = "" if success else "FAIL"
            self.add_info(message, self.check_results_layout, status=status)

        # Display required libraries in check results
        self.add_info("\nRequired Libraries:", self.check_results_layout)
        for lib in ['PyQt6', 'serial']:
            self.add_info(f"Library: {lib}", self.check_results_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    checker = SystemCheck()
    checker.run_checks()
    checker.show()
    sys.exit(app.exec())
