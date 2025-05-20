import sys
import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit
)

# tu robimy okienko do generowania kluczy ssh
class SSHKeyManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Key Generator")  # tytuł okna
        self.layout = QVBoxLayout()  # pionowy układ

        # pola do wpisywania danych
        self.email_input = QLineEdit()
        self.alias_input = QLineEdit()
        self.host_input = QLineEdit()

        self.layout.addWidget(QLabel("Email:"))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel("Alias:"))
        self.layout.addWidget(self.alias_input)
        self.layout.addWidget(QLabel("Host:"))
        self.layout.addWidget(self.host_input)

        # przycisk do generowania klucza
        self.generate_button = QPushButton("Generate Key")
        self.generate_button.clicked.connect(self.generate_ssh_key)
        self.layout.addWidget(self.generate_button)

        # przycisk żeby zobaczyć plik config
        self.show_config_button = QPushButton("Show config")
        self.show_config_button.clicked.connect(self.show_config)
        self.layout.addWidget(self.show_config_button)

        # przycisk żeby zobaczyć plik json z kluczami
        self.show_keys_json_button = QPushButton("Show .json")
        self.show_keys_json_button.clicked.connect(self.show_keys_json)
        self.layout.addWidget(self.show_keys_json_button)

        # przycisk do kopiowania folderu z kluczami gdzie indziej
        self.copy_button = QPushButton("Copy 'keys' to another folder")
        self.copy_button.clicked.connect(self.copy_keys_folder)
        self.layout.addWidget(self.copy_button)

        # pole gdzie będą pokazywane komunikaty
        self.output = QTextEdit()
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

        # ścieżki do folderu i plików
        self.keys_folder = Path("keys")
        self.config_path = self.keys_folder / "config"
        self.json_path = self.keys_folder / "keys.json"
        self.keys_folder.mkdir(exist_ok=True)  # tworzy folder jak nie ma

    # funkcja do generowania klucza ssh
    def generate_ssh_key(self):
        email = self.email_input.text().strip()
        alias = self.alias_input.text().strip()
        host = self.host_input.text().strip()

        if not all([email, alias, host]):
            self.output.setText("Wpisz wszystko: email, alias i host")
            return

        key_name = f"id_ed25519.{alias}"
        key_path = self.keys_folder / key_name

        # komenda do ssh-keygen, żeby stworzyć nowy klucz
        cmd = [
            "ssh-keygen", "-t", "ed25519", "-C", email,
            "-f", str(key_path), "-N", ""  # -N "" czyli bez hasła
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            self.output.setText("Coś poszło nie tak może klucz już jest")
            return

        # dopisujemy nowy wpis do configa ssh
        config_line = (
            f"Host {alias}\n"
            f"    HostName {host}\n"
            f"    User git\n"
            f"    IdentityFile {key_path}\n\n"
        )
        with open(self.config_path, "a") as config_file:
            config_file.write(config_line)

        # teraz dodajemy info o kluczu do keys.json
        keys = []
        if self.json_path.exists():
            with open(self.json_path, "r") as f:
                keys = json.load(f)

        keys.append({
            "key_name": key_name,
            "email": email,
            "hostname": host,
            "path": str(key_path),
            "timestamp": datetime.now().isoformat()
        })
        with open(self.json_path, "w") as f:
            json.dump(keys, f, indent=4)

        self.output.setText(f"Klucz '{key_name}' został zrobiony")

    # pokazuje zawartość pliku config
    def show_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                content = f.read()
            self.output.setText(content)
        else:
            self.output.setText("Nie ma pliku config")

    # pokazuje zawartość keys.json
    def show_keys_json(self):
        if self.json_path.exists():
            with open(self.json_path, "r") as f:
                content = f.read()
            self.output.setText(content)
        else:
            self.output.setText("Nie ma pliku .json")

    # kopiowanie całego folderu keys gdzie indziej
    def copy_keys_folder(self):
        dest_dir = QFileDialog.getExistingDirectory(self, "Wybierz folder docelowy")
        if dest_dir:
            try:
                target = Path(dest_dir) / "keys"
                if target.exists():
                    shutil.rmtree(target)  # usuwa jeśli już jest
                shutil.copytree(self.keys_folder, target)  # kopiuje cały folder
                self.output.setText(f"Folder skopiowany do {target}")
            except Exception as e:
                self.output.setText(f"Blad kopiowania: {e}")
        else:
            self.output.setText("Kopiowanie przerwane")

# odpala całe GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SSHKeyManager()
    window.show()
    sys.exit(app.exec_())
