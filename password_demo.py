import hashlib
import itertools
import time
from PyQt5 import QtWidgets, QtCore
import sys

# ---------------- HASH FUNCTION ---------------- #
def hash_password(password, algorithm):
    try:
        if algorithm == "MD5":
            return hashlib.md5(password.encode()).hexdigest()

        elif algorithm == "SHA1":
            return hashlib.sha1(password.encode()).hexdigest()

        elif algorithm == "NTLM":
            # NTLM = MD4 over UTF-16LE (may not exist on all systems)
            return hashlib.new("md4", password.encode("utf-16le")).hexdigest()

    except Exception:
        return None


# ---------------- BRUTE FORCE DEMO ---------------- #
def brute_force_demo(hash_value, algorithm):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    start_time = time.time()

    # Soft limit to avoid freezing system
    for length in range(1, 7):
        for pwd in itertools.product(chars, repeat=length):
            pwd = ''.join(pwd)
            hashed = hash_password(pwd, algorithm)

            if hashed and hashed == hash_value:
                return pwd, time.time() - start_time

    return "Not Found (Search Space Too Large)", time.time() - start_time


# ---------------- DICTIONARY DEMO ---------------- #
def dictionary_demo(hash_value, algorithm, dictionary_path):
    start_time = time.time()

    try:
        with open(dictionary_path, 'r', errors="ignore") as f:
            for line in f:
                pwd = line.strip()
                hashed = hash_password(pwd, algorithm)

                if hashed and hashed == hash_value:
                    return pwd, time.time() - start_time

    except Exception:
        return "Dictionary Error", 0

    return "Not Found in Dictionary", time.time() - start_time


# ---------------- WORKER THREAD ---------------- #
class PasswordDemoWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str, float)

    def __init__(self, hash_value, algorithm, mode, dictionary=None):
        super().__init__()
        self.hash_value = hash_value
        self.algorithm = algorithm
        self.mode = mode
        self.dictionary = dictionary

    def run(self):
        if self.mode == "Brute Force Demo":
            result, elapsed = brute_force_demo(self.hash_value, self.algorithm)
        else:
            result, elapsed = dictionary_demo(
                self.hash_value, self.algorithm, self.dictionary
            )

        self.finished.emit(result, elapsed)


# ---------------- GUI ---------------- #
class PasswordStrengthDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.dictionary = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Hash Strength Demonstrator")
        self.setGeometry(400, 300, 500, 330)

        layout = QtWidgets.QVBoxLayout()

        disclaimer = QtWidgets.QLabel(
            "Demonstrates Weak Password Risks"
        )
        layout.addWidget(disclaimer)

        self.hash_input = QtWidgets.QLineEdit()
        self.hash_input.setPlaceholderText("Enter MD5 / SHA1 / NTLM Hash")
        layout.addWidget(self.hash_input)

        self.algorithm = QtWidgets.QComboBox()
        self.algorithm.addItems(["MD5", "SHA1", "NTLM"])
        layout.addWidget(self.algorithm)

        self.mode = QtWidgets.QComboBox()
        self.mode.addItems(["Brute Force Demo", "Dictionary Demo"])
        layout.addWidget(self.mode)

        self.dict_btn = QtWidgets.QPushButton("Upload Dictionary File")
        self.dict_btn.clicked.connect(self.load_dictionary)
        layout.addWidget(self.dict_btn)

        self.start_btn = QtWidgets.QPushButton("Start Demo")
        self.start_btn.clicked.connect(self.start_demo)
        layout.addWidget(self.start_btn)

        self.result = QtWidgets.QLabel("")
        layout.addWidget(self.result)

        self.setLayout(layout)

    def load_dictionary(self):
        self.dictionary, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Dictionary", "", "Text Files (*.txt)"
        )

    def start_demo(self):
        hash_val = self.hash_input.text().strip()
        if not hash_val:
            self.result.setText("Please enter a hash value.")
            return

        self.result.setText("Running demo...")

        self.thread = QtCore.QThread()
        self.worker = PasswordDemoWorker(
            hash_val,
            self.algorithm.currentText(),
            self.mode.currentText(),
            self.dictionary
        )

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.show_result)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def show_result(self, password, time_taken):
        self.result.setText(
            f"Result: {password}\nTime Taken: {time_taken:.2f} seconds"
        )


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordStrengthDemo()
    window.show()
    sys.exit(app.exec_())
