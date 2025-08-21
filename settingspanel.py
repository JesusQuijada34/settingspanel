import sys, os, platform, shutil, subprocess, json, requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QStackedWidget,
    QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidgetItem,
    QLineEdit, QComboBox, QColorDialog, QFormLayout, QMessageBox, QSlider
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

CONFIG_DIR = "config"

GOOGLE_LANGS = {
    "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian", "az": "Azerbaijani",
    "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan",
    "ceb": "Cebuano", "zh-CN": "Chinese (Simplified)", "zh-TW": "Chinese (Traditional)", "co": "Corsican",
    "hr": "Croatian", "cs": "Czech", "da": "Danish", "nl": "Dutch", "en": "English", "eo": "Esperanto",
    "et": "Estonian", "fi": "Finnish", "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian",
    "de": "German", "el": "Greek", "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa", "haw": "Hawaiian",
    "he": "Hebrew", "hi": "Hindi", "hmn": "Hmong", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo",
    "id": "Indonesian", "ga": "Irish", "it": "Italian", "ja": "Japanese", "jw": "Javanese", "kn": "Kannada",
    "kk": "Kazakh", "km": "Khmer", "ko": "Korean", "ku": "Kurdish", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin",
    "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy",
    "ms": "Malay", "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian",
    "my": "Myanmar (Burmese)", "ne": "Nepali", "no": "Norwegian", "ny": "Nyanja (Chichewa)", "or": "Odia",
    "ps": "Pashto", "fa": "Persian", "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian",
    "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic", "sr": "Serbian", "st": "Sesotho", "sn": "Shona",
    "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali", "es": "Spanish",
    "su": "Sundanese", "sw": "Swahili", "sv": "Swedish", "tl": "Tagalog (Filipino)", "tg": "Tajik", "ta": "Tamil",
    "tt": "Tatar", "te": "Telugu", "th": "Thai", "tr": "Turkish", "tk": "Turkmen", "uk": "Ukrainian",
    "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish",
    "yo": "Yoruba", "zu": "Zulu"
}

class FlatrConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración del Sistema")
        self.setFixedSize(1000, 650)
        self.apps_dir = self.get_apps_directory()
        self.text_color = "#000000"
        self.button_color = "#0078D7"
        self.language = "es"
        self.translations = self.load_language(self.language)

        os.makedirs(CONFIG_DIR, exist_ok=True)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.stack = QStackedWidget()
        self.header = QLabel(self.t("Wi-Fi"))
        self.header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 12px;")
        self.sidebar.currentRowChanged.connect(self.update_section)

        self.sections = {
            self.t("Wi-Fi"): self.wifi_panel(),
            self.t("Bluetooth"): self.bluetooth_panel(),
            self.t("Aplicaciones"): self.apps_panel(),
            self.t("Almacenamiento"): self.storage_panel(),
            self.t("Tema"): self.theme_panel(),
            self.t("Pantalla y Batería"): self.display_battery_panel(),
            self.t("Idioma del sistema"): self.language_panel(),
            self.t("Actualizaciones"): self.update_panel(),
            self.t("Acerca del dispositivo"): self.about_panel()
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

    def t(self, key):
        """Translation helper"""
        return self.translations.get(key, key)

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

    # Wi-Fi Panel
    def wifi_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.t("Redes Wi-Fi disponibles:")))
        self.wifi_list = QComboBox()
        self.wifi_pass = QLineEdit()
        self.wifi_pass.setPlaceholderText(self.t("Contraseña"))
        self.wifi_pass.setEchoMode(QLineEdit.EchoMode.Password)
        connect_btn = QPushButton(self.t("Conectar"))
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
            layout.addWidget(QLabel(f"{self.t('Error al escanear redes')}: {e}"))

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
            QMessageBox.critical(self, self.t("Error"), f"{self.t('No se pudo conectar')}:\n{e}")

    # Bluetooth Panel
    def bluetooth_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.t("Bluetooth") + ":"))
        layout.addWidget(QLabel(self.t("Usa dongle o adaptador interno.")))
        panel.setLayout(layout)
        return panel

    # Apps Panel
    def apps_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.t("Aplicaciones instaladas:")))
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
            QMessageBox.information(self, self.t("Eliminado"), f"{self.t('Se eliminó la app')}:\n{os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, self.t("Error"), f"{self.t('No se pudo eliminar')}:\n{e}")

    # Storage Panel
    def storage_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        total, used, free = shutil.disk_usage("/")
        layout.addWidget(QLabel(f"{self.t('Total')}: {total // (2**30)} GB"))
        layout.addWidget(QLabel(f"{self.t('Usado')}: {used // (2**30)} GB"))
        layout.addWidget(QLabel(f"{self.t('Libre')}: {free // (2**30)} GB"))
        panel.setLayout(layout)
        return panel

    # Theme Panel
    def theme_panel(self):
        panel = QWidget()
        layout = QFormLayout()
        layout.addRow(QLabel(self.t("Color del texto") + ":"), self.color_picker("text"))
        layout.addRow(QLabel(self.t("Color de botones") + ":"), self.color_picker("button"))
        apply_btn = QPushButton(self.t("Aplicar tema"))
        apply_btn.clicked.connect(self.apply_theme)
        layout.addRow(apply_btn)
        panel.setLayout(layout)
        return panel

    def color_picker(self, target):
        btn = QPushButton(self.t("Seleccionar color"))
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

    # Display/Battery panel
    def display_battery_panel(self):
        panel = QWidget()
        layout = QFormLayout()
        # Brillo (simulado)
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(60)
        layout.addRow(QLabel(self.t("Brillo de pantalla")), self.brightness_slider)

        # Modo oscuro
        self.dark_mode_btn = QPushButton(self.t("Alternar modo oscuro"))
        self.dark_mode_btn.setCheckable(True)
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        layout.addRow(self.dark_mode_btn)

        # Batería (simulada)
        battery_level = self.get_battery_level()
        layout.addRow(QLabel(self.t("Nivel de batería")), QLabel(f"{battery_level}%"))

        panel.setLayout(layout)
        return panel

    def toggle_dark_mode(self):
        if self.dark_mode_btn.isChecked():
            self.setStyleSheet("QMainWindow { background-color: #222; color: #fff; } QLabel { color: #fff; }")
            self.dark_mode_btn.setText(self.t("Modo claro"))
        else:
            self.apply_theme()
            self.dark_mode_btn.setText(self.t("Modo oscuro"))

    def get_battery_level(self):
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                return int(battery.percent)
            else:
                return 100
        except:
            return 100

    # Language panel
    def language_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.t("Selecciona el idioma del sistema:")))
        self.lang_combo = QComboBox()
        for code, name in GOOGLE_LANGS.items():
            self.lang_combo.addItem(f"{name} ({code})", code)
        # Selecciona actual
        if self.language in GOOGLE_LANGS:
            self.lang_combo.setCurrentText(f"{GOOGLE_LANGS[self.language]} ({self.language})")
        layout.addWidget(self.lang_combo)

        self.lang_status = QLabel("")
        layout.addWidget(self.lang_status)
        apply_btn = QPushButton(self.t("Aplicar idioma"))
        apply_btn.clicked.connect(self.change_language)
        layout.addWidget(apply_btn)
        panel.setLayout(layout)
        return panel

    def change_language(self):
        code = self.lang_combo.currentData()
        lang_file = os.path.join(CONFIG_DIR, f"{code}.json")
        if not os.path.exists(lang_file):
            if self.check_internet():
                self.lang_status.setText(self.t("Descargando idioma..."))
                QApplication.processEvents()
                self.download_language(code)
            else:
                self.lang_status.setText(self.t("No hay conexión. Solo idiomas instalados disponibles."))
                return
        self.language = code
        self.translations = self.load_language(self.language)
        self.lang_status.setText(self.t("Idioma cambiado"))
        self.refresh_ui()

    def download_language(self, code):
        base_keys = [
            "Wi-Fi", "Bluetooth", "Aplicaciones", "Almacenamiento", "Tema", "Pantalla y Batería",
            "Idioma del sistema", "Actualizaciones", "Acerca del dispositivo",
            "Redes Wi-Fi disponibles:", "Contraseña", "Conectar", "Error al escanear redes",
            "Error", "No se pudo conectar", "Aplicaciones instaladas:", "Eliminado",
            "Se eliminó la app", "No se pudo eliminar", "Total", "Usado", "Libre",
            "Color del texto", "Color de botones", "Aplicar tema", "Seleccionar color",
            "Brillo de pantalla", "Alternar modo oscuro", "Modo oscuro", "Modo claro",
            "Nivel de batería", "Selecciona el idioma del sistema:", "Aplicar idioma",
            "Descargando idioma...", "No hay conexión. Solo idiomas instalados disponibles.",
            "Idioma cambiado", "Buscar actualizaciones", "Verifica y aplica actualizaciones del sistema.",
            "Buscando actualizaciones...", "Nueva versión disponible: 1.1.0", "Descargar e instalar",
            "Descargando e instalando actualización...", "Actualización instalada. Reinicie para aplicar cambios.",
            "Sistema", "Arquitectura"
        ]
        translations = {}
        for key in base_keys:
            translated = self.translate_text(key, "es", code)
            translations[key] = translated
        lang_file = os.path.join(CONFIG_DIR, f"{code}.json")
        with open(lang_file, "w", encoding="utf-8") as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)

    def load_language(self, code):
        lang_file = os.path.join(CONFIG_DIR, f"{code}.json")
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def translate_text(self, text, from_lang, to_lang):
        try:
            response = requests.get(
                f"https://translate.googleapis.com/translate_a/single",
                params={
                    "client": "gtx",
                    "sl": from_lang,
                    "tl": to_lang,
                    "dt": "t",
                    "q": text
                }
            )
            data = response.json()
            return data[0][0][0]
        except Exception as e:
            return text

    def check_internet(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def refresh_ui(self):
        self.sidebar.clear()
        self.sections = {
            self.t("Wi-Fi"): self.wifi_panel(),
            self.t("Bluetooth"): self.bluetooth_panel(),
            self.t("Aplicaciones"): self.apps_panel(),
            self.t("Almacenamiento"): self.storage_panel(),
            self.t("Tema"): self.theme_panel(),
            self.t("Pantalla y Batería"): self.display_battery_panel(),
            self.t("Idioma del sistema"): self.language_panel(),
            self.t("Actualizaciones"): self.update_panel(),
            self.t("Acerca del dispositivo"): self.about_panel()
        }
        for name, widget in self.sections.items():
            item = QListWidgetItem(name)
            self.sidebar.addItem(item)
            self.stack.addWidget(widget)
        self.header.setText(self.sidebar.item(self.sidebar.currentRow()).text())

    # Update (system update) panel
    def update_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.t("Verifica y aplica actualizaciones del sistema.")))
        check_btn = QPushButton(self.t("Buscar actualizaciones"))
        check_btn.clicked.connect(self.check_updates)
        self.update_status = QLabel("")
        layout.addWidget(check_btn)
        layout.addWidget(self.update_status)
        panel.setLayout(layout)
        return panel

    def check_updates(self):
        self.update_status.setText(self.t("Buscando actualizaciones..."))
        QApplication.processEvents()
        import time; time.sleep(2)
        self.update_status.setText(self.t("Nueva versión disponible: 1.1.0"))
        update_btn = QPushButton(self.t("Descargar e instalar"))
        update_btn.clicked.connect(self.install_update)
        layout = self.update_status.parentWidget().layout()
        layout.addWidget(update_btn)

    def install_update(self):
        self.update_status.setText(self.t("Descargando e instalando actualización..."))
        QApplication.processEvents()
        import time; time.sleep(3)
        self.update_status.setText(self.t("Actualización instalada. Reinicie para aplicar cambios."))

    def about_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{self.t('Sistema')}: {platform.system()} {platform.release()}"))
        layout.addWidget(QLabel(f"{self.t('Arquitectura')}: {platform.machine()}"))
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
    sys.exit(app.exec())            item = QListWidgetItem(name)
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
