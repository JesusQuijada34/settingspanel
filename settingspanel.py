# flatr_configurator.py
import sys, os, platform, shutil, subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QStackedWidget,
    QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidgetItem,
    QLineEdit, QComboBox, QColorDialog, QFormLayout, QScrollArea
)
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtCore import Qt

class FlatrConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración del Sistema")
        self.setFixedSize(1000, 650)
        self.apps_dir = self.get_apps_directory()
        self.text_color = "#000000"
        self.button_color = "#0078D7"

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.stack = QStackedWidget()
        self.header = QLabel("Wi-Fi")
        self.header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 12px;")
        self.sidebar.currentRowChanged.connect(self.update_section)

        self.sections = {
            "Wi-Fi": self.wifi_panel(),
            "Bluetooth": self.bluetooth_panel(),
            "Aplicaciones": self.apps_panel(),
            "Almacenamiento": self.storage_panel(),
            "Tema": self.theme_panel(),
            "Acerca del dispositivo": self.about_panel()
        }

        for name, widget in self.sections.items():
            item = QListWidgetItem(name)
            self.sidebar.addItem(item)
            self.stack.addWidget(widget)

        self.sidebar.setCurrentRow(0)

        content = QVBoxLayout()
        content.addWidget(self.header)
        content.addWidget(self.stack)

        layout = QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addLayout(content)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.apply_theme()

    def update_section(self, index):
        self.stack.setCurrentIndex(index)
        self.header.setText(self.sidebar.item(index).text())

    def apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #f0f0f0; }}
            QLabel {{ color: {self.text_color}; font-size: 14px; }}
            QPushButton {{
                background-color: {self.button_color};
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{ background-color: #005A9E; }}
            QListWidget {{ background-color: #e0e0e0; border: none; }}
            QListWidget::item {{ padding: 12px; }}
            QListWidget::item:selected {{ background-color: #ffffff; }}
        """)

    def wifi_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Redes Wi-Fi disponibles:"))
        self.wifi_list = QComboBox()
        self.wifi_pass = QLineEdit()
        self.wifi_pass.setPlaceholderText("Contraseña")
        self.wifi_pass.setEchoMode(QLineEdit.EchoMode.Password)
        connect_btn = QPushButton("Conectar")
        connect_btn.clicked.connect(self.connect_wifi)

        try:
            if os.name == "nt":
                result = subprocess.check_output("netsh wlan show networks", shell=True).decode()
                for line in result.splitlines():
                    if "SSID" in line:
                        ssid = line.split(":")[1].strip()
                        self.wifi_list.addItem(ssid)
            else:
                result = subprocess.check_output("nmcli -t -f SSID dev wifi", shell=True).decode()
                for ssid in result.splitlines():
                    if ssid:
                        self.wifi_list.addItem(ssid.strip())
        except Exception as e:
            layout.addWidget(QLabel(f"Error al escanear redes: {e}"))

        layout.addWidget(self.wifi_list)
        layout.addWidget(self.wifi_pass)
        layout.addWidget(connect_btn)
        panel.setLayout(layout)
        return panel

    def connect_wifi(self):
        ssid = self.wifi_list.currentText()
        password = self.wifi_pass.text()
        try:
            if os.name == "nt":
                subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True)
            else:
                subprocess.run(f'nmcli dev wifi connect "{ssid}" password "{password}"', shell=True)
            self.wifi_pass.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar:\n{e}")

    def bluetooth_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bluetooth:"))
        layout.addWidget(QLabel("Usa dongle o adaptador interno."))
        panel.setLayout(layout)
        return panel

    def apps_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aplicaciones instaladas:"))
        for folder in os.listdir(self.apps_dir):
            path = os.path.join(self.apps_dir, folder)
            if os.path.isdir(path):
                size = self.get_folder_size(path)
                btn = QPushButton(f"{folder} ({size} MB)")
                btn.clicked.connect(lambda _, p=path: self.remove_app(p))
                if size > 100:  # apps pesadas
                    btn.setStyleSheet("background-color: #ff5555; color: white;")
                layout.addWidget(btn)
        panel.setLayout(layout)
        return panel

    def remove_app(self, path):
        try:
            shutil.rmtree(path)
            QMessageBox.information(self, "Eliminado", f"Se eliminó la app:\n{os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar:\n{e}")

    def storage_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        total, used, free = shutil.disk_usage("/")
        layout.addWidget(QLabel(f"Total: {total // (2**30)} GB"))
        layout.addWidget(QLabel(f"Usado: {used // (2**30)} GB"))
        layout.addWidget(QLabel(f"Libre: {free // (2**30)} GB"))
        panel.setLayout(layout)
        return panel

    def theme_panel(self):
        panel = QWidget()
        layout = QFormLayout()
        layout.addRow(QLabel("Color del texto:"), self.color_picker("text"))
        layout.addRow(QLabel("Color de botones:"), self.color_picker("button"))
        apply_btn = QPushButton("Aplicar tema")
        apply_btn.clicked.connect(self.apply_theme)
        layout.addRow(apply_btn)
        panel.setLayout(layout)
        return panel

    def color_picker(self, target):
        btn = QPushButton("Seleccionar color")
        def pick():
            color = QColorDialog.getColor()
            if color.isValid():
                hex_color = color.name()
                if target == "text":
                    self.text_color = hex_color
                else:
                    self.button_color = hex_color
        btn.clicked.connect(pick)
        return btn

    def about_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Sistema: {platform.system()} {platform.release()}"))
        layout.addWidget(QLabel(f"Arquitectura: {platform.machine()}"))
        layout.addWidget(QLabel(f"Python: {platform.python_version()}"))
        panel.setLayout(layout)
        return panel

    def get_apps_directory(self):
        if os.name == "nt":
            from ctypes import windll, create_unicode_buffer
            buf = create_unicode_buffer(260)
            windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
            return os.path.join(buf.value, "Flatr Apps")
        else:
            return os.path.expanduser("~/Documentos/Flatr Apps")

    def get_folder_size(self, path):
        total = 0
        for root, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return round(total / (1024 * 1024), 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlatrConfigurator()
    window.show()
    sys.exit(app.exec())
