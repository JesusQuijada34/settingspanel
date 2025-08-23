import sys
import os
import json
import subprocess
import platform
import pygame
import pygame.gfxdraw
import math
import time
from pygame.locals import *

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Universal System Tweaker")

# Colores
GITHUB_LIGHT = {
    'bg': (246, 248, 250),
    'card': (255, 255, 255),
    'text': (36, 41, 46),
    'text_secondary': (88, 96, 105),
    'primary': (3, 102, 214),
    'success': (40, 167, 69),
    'border': (225, 228, 232),
    'hover': (243, 244, 246),
    'tab_bg': (241, 243, 245),
    'tab_active': (255, 255, 255)
}

GITHUB_DARK = {
    'bg': (22, 27, 34),
    'card': (33, 38, 45),
    'text': (240, 246, 252),
    'text_secondary': (139, 148, 158),
    'primary': (47, 129, 247),
    'success': (87, 171, 90),
    'border': (48, 54, 61),
    'hover': (48, 54, 61),
    'tab_bg': (33, 38, 45),
    'tab_active': (48, 54, 61)
}

# Cargar configuración de tema
def load_theme_config():
    try:
        if os.path.exists("theme_config.json"):
            with open("theme_config.json", "r") as f:
                config = json.load(f)
                return config.get("dark_mode", False)
    except:
        pass
    return False

# Guardar configuración de tema
def save_theme_config(dark_mode):
    config = {"dark_mode": dark_mode}
    with open("theme_config.json", "w") as f:
        json.dump(config, f)

# Cargar configuración de idioma
def load_language_config():
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                return config.get("language", "en"), config.get("remember", False)
    except:
        pass
    return "en", False

# Guardar configuración de idioma
def save_language_config(language, remember):
    config = {"language": language, "remember": remember}
    with open("config.json", "w") as f:
        json.dump(config, f)

# Traducciones
translations = {
    "en": {
        "title": "Universal System Tweaker",
        "select_language": "Select your language",
        "remember_choice": "Remember my choice",
        "continue": "Continue",
        "windows_tweaks": "Windows Tweaks",
        "linux_tweaks": "Linux Tweaks",
        "terminal_output": "Terminal Output",
        "performance_optimization": "Performance Optimization",
        "disable_animations": "Disable unnecessary animations",
        "prefetch_tweaks": "Optimize Prefetch configuration",
        "disable_tips": "Disable Windows tips",
        "privacy_settings": "Privacy Settings",
        "disable_telemetry": "Limit telemetry",
        "disable_ads": "Disable built-in advertising",
        "apply_selected": "Apply selected changes",
        "basic_linux_settings": "Basic Linux Settings",
        "enable_ufw": "Enable firewall (UFW)",
        "install_updates": "Install available updates",
        "clean_packages": "Clean unnecessary packages",
        "terminal_placeholder": "Terminal output will appear here",
        "applying_settings": "Applying settings...",
        "settings_applied": "Settings applied successfully!",
        "select_option": "Please select at least one option",
        "theme_toggle": "Toggle Dark/Light Mode",
        "back": "Back"
    },
    "es": {
        "title": "Configurador Universal de Sistema",
        "select_language": "Selecciona tu idioma",
        "remember_choice": "Recordar mi elección",
        "continue": "Continuar",
        "windows_tweaks": "Ajustes de Windows",
        "linux_tweaks": "Ajustes de Linux",
        "terminal_output": "Salida del Terminal",
        "performance_optimization": "Optimización de Rendimiento",
        "disable_animations": "Deshabilitar animaciones innecesarias",
        "prefetch_tweaks": "Optimizar configuración Prefetch",
        "disable_tips": "Deshabilitar sugerencias de Windows",
        "privacy_settings": "Ajustes de Privacidad",
        "disable_telemetry": "Limitar telemetría",
        "disable_ads": "Deshabilitar publicidad integrada",
        "apply_selected": "Aplicar cambios",
        "basic_linux_settings": "Ajustes Básicos de Linux",
        "enable_ufw": "Habilitar firewall (UFW)",
        "install_updates": "Instalar actualizaciones disponibles",
        "clean_packages": "Limpiar paquetes innecesarios",
        "terminal_placeholder": "La salida del terminal aparecerá aquí",
        "applying_settings": "Aplicando configuración...",
        "settings_applied": "¡Configuración aplicada con éxito!",
        "select_option": "Por favor seleccione al menos una opción",
        "theme_toggle": "Cambiar Modo Oscuro/Claro",
        "back": "Volver"
    },
    "fr": {
        "title": "Optimiseur Universel de Système",
        "select_language": "Sélectionnez votre langue",
        "remember_choice": "Se souvenir de mon choix",
        "continue": "Continuer",
        "windows_tweaks": "Réglages Windows",
        "linux_tweaks": "Réglages Linux",
        "terminal_output": "Sortie Terminal",
        "performance_optimization": "Optimisation des Performances",
        "disable_animations": "Désactiver les animations inutiles",
        "prefetch_tweaks": "Optimiser la configuration Prefetch",
        "disable_tips": "Désactiver les conseils Windows",
        "privacy_settings": "Paramètres de Confidentialité",
        "disable_telemetry": "Limiter la télémétrie",
        "disable_ads": "Désactiver la publicité intégrée",
        "apply_selected": "Appliquer les modifications sélectionnées",
        "basic_linux_settings": "Paramètres Linux de Base",
        "enable_ufw": "Activer le pare-feu (UFW)",
        "install_updates": "Installer les mises à jour disponibles",
        "clean_packages": "Nettoyer les paquets inutiles",
        "terminal_placeholder": "La sortie du terminal apparaîtra ici",
        "applying_settings": "Application des paramètres...",
        "settings_applied": "Paramètres appliqués avec succès!",
        "select_option": "Veuillez sélectionner au moins une option",
        "theme_toggle": "Changer Mode Sombre/Clair",
        "back": "Retour"
    },
    "de": {
        "title": "Universal System Optimizer",
        "select_language": "Wählen Sie Ihre Sprache",
        "remember_choice": "Meine Wahl merken",
        "continue": "Fortfahren",
        "windows_tweaks": "Windows-Einstellungen",
        "linux_tweaks": "Linux-Einstellungen",
        "terminal_output": "Terminalausgabe",
        "performance_optimization": "Leistungsoptimierung",
        "disable_animations": "Unnötige Animationen deaktivieren",
        "prefetch_tweaks": "Prefetch-Konfiguration optimieren",
        "disable_tips": "Windows-Tipps deaktivieren",
        "privacy_settings": "Datenschutzeinstellungen",
        "disable_telemetry": "Telemetrie einschränken",
        "disable_ads": "Eingebaute Werbung deaktivieren",
        "apply_selected": "Ausgewählte Änderungen übernehmen",
        "basic_linux_settings": "Grundlegende Linux-Einstellungen",
        "enable_ufw": "Firewall aktivieren (UFW)",
        "install_updates": "Verfügbare Updates installieren",
        "clean_packages": "Unnötige Pakete bereinigen",
        "terminal_placeholder": "Terminalausgabe wird hier angezeigt",
        "applying_settings": "Einstellungen werden übernommen...",
        "settings_applied": "Einstellungen erfolgreich übernommen!",
        "select_option": "Bitte wählen Sie mindestens eine Option",
        "theme_toggle": "Dunkel/Hell-Modus umschalten",
        "back": "Zurück"
    },
    "it": {
        "title": "Ottimizzatore Universale di Sistema",
        "select_language": "Seleziona la tua lingua",
        "remember_choice": "Ricorda la mia scelta",
        "continue": "Continua",
        "windows_tweaks": "Ottimizzazioni Windows",
        "linux_tweaks": "Ottimizzazioni Linux",
        "terminal_output": "Output Terminale",
        "performance_optimization": "Ottimizzazione Prestazioni",
        "disable_animations": "Disabilita animazioni non necessarie",
        "prefetch_tweaks": "Ottimizza configurazione Prefetch",
        "disable_tips": "Disabilita suggerimenti Windows",
        "privacy_settings": "Impostazioni Privacy",
        "disable_telemetry": "Limita telemetria",
        "disable_ads": "Disabilita pubblicità incorporata",
        "apply_selected": "Applica modifiche selezionate",
        "basic_linux_settings": "Impostazioni Base Linux",
        "enable_ufw": "Abilita firewall (UFW)",
        "install_updates": "Installa aggiornamenti disponibili",
        "clean_packages": "Pulisci pacchetti non necessari",
        "terminal_placeholder": "L'output del terminale apparirà qui",
        "applying_settings": "Applicazione impostazioni...",
        "settings_applied": "Impostazioni applicate con successo!",
        "select_option": "Seleziona almeno un'opzione",
        "theme_toggle": "Attiva/Disattiva Modalità Scura/Chiara",
        "back": "Indietro"
    }
}

# Clase para partículas animadas
class Particle:
    def __init__(self, x, y, color, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.lifetime = 100 + 100 * (time.time() % 1)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        alpha = min(255, int(self.lifetime * 2.55))
        color_with_alpha = (*self.color, alpha)
        pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.size), color_with_alpha)

# Clase para botones personalizados
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font, action=None, border_radius=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.action = action
        self.border_radius = border_radius
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.text_color, self.rect, width=1, border_radius=self.border_radius)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.action:
                self.action()
            return True
        return False

# Clase para checkbox personalizados
class Checkbox:
    def __init__(self, x, y, text, text_color, font, checked=False, action=None):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.text = text
        self.text_color = text_color
        self.font = font
        self.checked = checked
        self.action = action
        self.hovered = False

    def draw(self, surface, theme):
        # Dibujar checkbox
        border_color = theme['primary'] if self.hovered else theme['border']
        pygame.draw.rect(surface, border_color, self.rect, width=1, border_radius=4)

        if self.checked:
            pygame.draw.rect(surface, theme['primary'], self.rect, border_radius=4)
            # Dibujar marca de verificación
            pygame.draw.line(surface, theme['card'],
                            (self.rect.x + 4, self.rect.y + 10),
                            (self.rect.x + 8, self.rect.y + 14), 2)
            pygame.draw.line(surface, theme['card'],
                            (self.rect.x + 8, self.rect.y + 14),
                            (self.rect.x + 16, self.rect.y + 6), 2)

        # Dibujar texto
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + 30, self.rect.y))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.checked = not self.checked
            if self.action:
                self.action(self.checked)
            return True
        return False

# Clase para grupo de controles
class ControlGroup:
    def __init__(self, x, y, width, height, title, theme, font_title, font_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.theme = theme
        self.font_title = font_title
        self.font_text = font_text
        self.controls = []

    def add_checkbox(self, text, action=None):
        y_pos = self.rect.y + 40 + len(self.controls) * 30
        checkbox = Checkbox(self.rect.x + 20, y_pos, text, self.theme['text'], self.font_text, action=action)
        self.controls.append(checkbox)
        return checkbox

    def draw(self, surface):
        # Dibujar fondo del grupo
        pygame.draw.rect(surface, self.theme['card'], self.rect, border_radius=8)
        pygame.draw.rect(surface, self.theme['border'], self.rect, width=1, border_radius=8)

        # Dibujar título
        title_surface = self.font_title.render(self.title, True, self.theme['text'])
        surface.blit(title_surface, (self.rect.x + 15, self.rect.y + 10))

        # Dibujar controles
        for control in self.controls:
            control.draw(surface, self.theme)

    def handle_event(self, event):
        for control in self.controls:
            if control.handle_event(event):
                return True
        return False

    def check_hover(self, pos):
        for control in self.controls:
            control.check_hover(pos)

# Clase para terminal de salida
class Terminal:
    def __init__(self, x, y, width, height, theme, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.theme = theme
        self.font = font
        self.lines = []
        self.scroll_offset = 0
        self.placeholder = ""

    def add_line(self, line):
        self.lines.append(line)
        # Auto-scroll to bottom
        self.scroll_offset = max(0, len(self.lines) * 20 - self.rect.height + 40)

    def set_placeholder(self, text):
        self.placeholder = text

    def draw(self, surface):
        # Dibujar fondo del terminal
        pygame.draw.rect(surface, self.theme['card'], self.rect, border_radius=8)
        pygame.draw.rect(surface, self.theme['border'], self.rect, width=1, border_radius=8)

        # Dibujar contenido
        content_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 20, self.rect.height - 20)

        if not self.lines:
            # Mostrar placeholder si no hay contenido
            placeholder_surface = self.font.render(self.placeholder, True, self.theme['text_secondary'])
            surface.blit(placeholder_surface, (content_rect.x, content_rect.y))
        else:
            # Mostrar líneas de contenido
            for i, line in enumerate(self.lines):
                y_pos = content_rect.y + i * 20 - self.scroll_offset
                if y_pos + 20 >= self.rect.y and y_pos <= self.rect.y + self.rect.height:
                    line_surface = self.font.render(line, True, self.theme['text'])
                    surface.blit(line_surface, (content_rect.x, y_pos))

# Clase para la aplicación principal
class SystemTweakerApp:
    def __init__(self):
        self.dark_mode = load_theme_config()
        self.theme = GITHUB_DARK if self.dark_mode else GITHUB_LIGHT
        self.language, self.remember_language = load_language_config()
        self.translations = translations.get(self.language, translations['en'])
        self.os_type = platform.system()

        # Fuentes
        self.font_large = pygame.font.SysFont("Arial", 24)
        self.font_medium = pygame.font.SysFont("Arial", 18)
        self.font_small = pygame.font.SysFont("Arial", 14)
        self.font_mono = pygame.font.SysFont("Courier New", 12)

        # Estados de la aplicación
        self.current_screen = "language"  # language, main, terminal
        self.particles = []

        # Inicializar controles según pantalla
        self.init_language_screen()

    def init_language_screen(self):
        self.current_screen = "language"
        self.language_buttons = []
        self.remember_checkbox = None
        self.continue_button = None

        languages = [
            ("English", "en", (3, 102, 214)),
            ("Español", "es", (40, 167, 69)),
            ("Français", "fr", (111, 66, 193)),
            ("Deutsch", "de", (255, 211, 61)),
            ("Italiano", "it", (234, 74, 90))
        ]

        # Crear botones de idioma
        for i, (name, code, color) in enumerate(languages):
            x = 200 + (i % 3) * 200
            y = 200 + (i // 3) * 120
            btn = Button(x, y, 180, 100, name, self.theme['card'], self.theme['hover'],
                        color, self.font_medium, lambda c=code: self.select_language(c))
            self.language_buttons.append(btn)

        # Crear checkbox para recordar elección
        self.remember_checkbox = Checkbox(400, 450, self.translations['remember_choice'],
                                         self.theme['text'], self.font_small, False)

        # Crear botón continuar
        self.continue_button = Button(400, 500, 200, 40, self.translations['continue'],
                                     self.theme['success'], (35, 134, 54),
                                     (255, 255, 255), self.font_medium, self.go_to_main_screen)

    def init_main_screen(self):
        self.current_screen = "main"

        # Crear botón de tema
        self.theme_button = Button(20, 20, 200, 40, self.translations['theme_toggle'],
                                  self.theme['card'], self.theme['hover'], self.theme['text'],
                                  self.font_small, self.toggle_theme)

        # Crear botón de terminal
        self.terminal_button = Button(WIDTH - 220, 20, 200, 40, self.translations['terminal_output'],
                                     self.theme['card'], self.theme['hover'], self.theme['text'],
                                     self.font_small, self.go_to_terminal_screen)

        # Crear grupos de controles según el sistema operativo
        if self.os_type == "Windows":
            self.control_groups = [
                ControlGroup(50, 100, 400, 250, self.translations['performance_optimization'],
                            self.theme, self.font_medium, self.font_small),
                ControlGroup(50, 370, 400, 180, self.translations['privacy_settings'],
                            self.theme, self.font_medium, self.font_small)
            ]

            # Añadir controles de Windows
            self.windows_controls = {
                'disable_animations': self.control_groups[0].add_checkbox(self.translations['disable_animations']),
                'prefetch_tweaks': self.control_groups[0].add_checkbox(self.translations['prefetch_tweaks']),
                'disable_tips': self.control_groups[0].add_checkbox(self.translations['disable_tips']),
                'disable_telemetry': self.control_groups[1].add_checkbox(self.translations['disable_telemetry']),
                'disable_ads': self.control_groups[1].add_checkbox(self.translations['disable_ads'])
            }

        elif self.os_type == "Linux":
            self.control_groups = [
                ControlGroup(50, 100, 400, 200, self.translations['basic_linux_settings'],
                            self.theme, self.font_medium, self.font_small)
            ]

            # Añadir controles de Linux
            self.linux_controls = {
                'enable_ufw': self.control_groups[0].add_checkbox(self.translations['enable_ufw']),
                'install_updates': self.control_groups[0].add_checkbox(self.translations['install_updates']),
                'clean_packages': self.control_groups[0].add_checkbox(self.translations['clean_packages'])
            }

        # Crear botón de aplicar
        self.apply_button = Button(WIDTH - 220, HEIGHT - 70, 200, 40, self.translations['apply_selected'],
                                  self.theme['success'], (35, 134, 54), (255, 255, 255),
                                  self.font_medium, self.apply_settings)

    def init_terminal_screen(self):
        self.current_screen = "terminal"

        # Crear terminal
        self.terminal = Terminal(50, 100, WIDTH - 100, HEIGHT - 200, self.theme, self.font_mono)
        self.terminal.set_placeholder(self.translations['terminal_placeholder'])

        # Crear botón de volver
        self.back_button = Button(50, HEIGHT - 70, 200, 40, self.translations['back'],
                                 self.theme['card'], self.theme['hover'], self.theme['text'],
                                 self.font_medium, self.go_to_main_screen)

    def select_language(self, language):
        self.language = language
        self.translations = translations.get(self.language, translations['en'])

        # Actualizar textos de los controles
        if hasattr(self, 'remember_checkbox'):
            self.remember_checkbox.text = self.translations['remember_choice']
        if hasattr(self, 'continue_button'):
            self.continue_button.text = self.translations['continue']

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme = GITHUB_DARK if self.dark_mode else GITHUB_LIGHT
        save_theme_config(self.dark_mode)

        # Recrear controles con el nuevo tema
        if self.current_screen == "main":
            self.init_main_screen()
        elif self.current_screen == "terminal":
            self.init_terminal_screen()

    def go_to_main_screen(self):
        if self.current_screen == "language" and self.remember_checkbox:
            save_language_config(self.language, self.remember_checkbox.checked)

        self.init_main_screen()

    def go_to_terminal_screen(self):
        self.init_terminal_screen()

    def apply_settings(self):
        commands = []

        if self.os_type == "Windows":
            if self.windows_controls['disable_animations'].checked:
                commands.extend([
                    'reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f',
                    'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v EnableTransparency /t REG_DWORD /d 0 /f'
                ])

            if self.windows_controls['prefetch_tweaks'].checked:
                commands.append('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 1 /f')

            if self.windows_controls['disable_tips'].checked:
                commands.append('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-310093Enabled /t REG_DWORD /d 0 /f')

            if self.windows_controls['disable_telemetry'].checked:
                commands.extend([
                    'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
                    'reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f'
                ])

            if self.windows_controls['disable_ads'].checked:
                commands.append('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')

        elif self.os_type == "Linux":
            if self.linux_controls['enable_ufw'].checked:
                commands.extend([
                    'sudo ufw enable',
                    'sudo systemctl enable ufw'
                ])

            if self.linux_controls['install_updates'].checked:
                commands.extend([
                    'sudo apt update',
                    'sudo apt upgrade -y'
                ])

            if self.linux_controls['clean_packages'].checked:
                commands.extend([
                    'sudo apt autoremove -y',
                    'sudo apt autoclean -y'
                ])

        if commands:
            self.go_to_terminal_screen()
            self.terminal.add_line(f"{self.translations['applying_settings']}")

            # Ejecutar comandos
            for cmd in commands:
                self.terminal.add_line(f"> {cmd}")

                try:
                    if self.os_type == "Windows":
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                    else:
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

                    if result.stdout:
                        for line in result.stdout.split('\n'):
                            if line.strip():
                                self.terminal.add_line(line)
                    if result.stderr:
                        for line in result.stderr.split('\n'):
                            if line.strip():
                                self.terminal.add_line(f"Error: {line}")

                except subprocess.TimeoutExpired:
                    self.terminal.add_line("Command timed out.")
                except Exception as e:
                    self.terminal.add_line(f"Exception: {str(e)}")

                self.terminal.add_line("-" * 50)

            self.terminal.add_line(f"{self.translations['settings_applied']}")
        else:
            # Mostrar mensaje de que no se seleccionó ninguna opción
            self.terminal.add_line(f"{self.translations['select_option']}")

    def add_particle(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        color = (84, 174, 255) if time.time() % 2 < 1 else (255, 118, 117)
        size = 3 + 7 * (time.time() % 1)
        speed_x = (time.time() % 1) - 0.5
        speed_y = (time.time() % 1) - 0.5

        self.particles.append(Particle(x, y, color, size, speed_x, speed_y))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            current_time = time.time()
            mouse_pos = pygame.mouse.get_pos()

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                # Manejar eventos según la pantalla actual
                if self.current_screen == "language":
                    for btn in self.language_buttons:
                        btn.handle_event(event)
                    if self.remember_checkbox:
                        self.remember_checkbox.handle_event(event)
                    if self.continue_button:
                        self.continue_button.handle_event(event)

                elif self.current_screen == "main":
                    self.theme_button.handle_event(event)
                    self.terminal_button.handle_event(event)
                    self.apply_button.handle_event(event)
                    for group in self.control_groups:
                        group.handle_event(event)

                elif self.current_screen == "terminal":
                    self.back_button.handle_event(event)

            # Actualizar partículas
            if current_time % 0.1 < 0.05:
                self.add_particle()

            self.particles = [p for p in self.particles if p.update()]

            # Dibujar fondo
            screen.fill(self.theme['bg'])

            # Dibujar partículas
            for particle in self.particles:
                particle.draw(screen)

            # Dibujar interfaz según la pantalla actual
            if self.current_screen == "language":
                # Dibujar título
                title_surface = self.font_large.render(self.translations['title'], True, self.theme['text'])
                screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

                subtitle_surface = self.font_medium.render(self.translations['select_language'], True, self.theme['text_secondary'])
                screen.blit(subtitle_surface, (WIDTH // 2 - subtitle_surface.get_width() // 2, 100))

                # Dibujar controles
                for btn in self.language_buttons:
                    btn.check_hover(mouse_pos)
                    btn.draw(screen)

                if self.remember_checkbox:
                    self.remember_checkbox.check_hover(mouse_pos)
                    self.remember_checkbox.draw(screen, self.theme)

                if self.continue_button:
                    self.continue_button.check_hover(mouse_pos)
                    self.continue_button.draw(screen)

            elif self.current_screen == "main":
                # Dibujar título
                title_surface = self.font_large.render(self.translations['title'], True, self.theme['text'])
                screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

                # Dibujar controles
                self.theme_button.check_hover(mouse_pos)
                self.theme_button.draw(screen)

                self.terminal_button.check_hover(mouse_pos)
                self.terminal_button.draw(screen)

                for group in self.control_groups:
                    group.check_hover(mouse_pos)
                    group.draw(screen)

                self.apply_button.check_hover(mouse_pos)
                self.apply_button.draw(screen)

            elif self.current_screen == "terminal":
                # Dibujar título
                title_surface = self.font_large.render(self.translations['terminal_output'], True, self.theme['text'])
                screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

                # Dibujar terminal
                self.terminal.draw(screen)

                # Dibujar botón de volver
                self.back_button.check_hover(mouse_pos)
                self.back_button.draw(screen)

            # Actualizar pantalla
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = SystemTweakerApp()
    app.run()
