¡Perfecto! Aquí tienes el README para tu SettingsPanel. Mientras buscas tu script, voy preparando esto:

---

# SettingsPanel - Configurador Universal de Sistema

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![PyGame](https://img.shields.io/badge/PyGame-2.5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Una aplicación moderna y elegante para optimizar y configurar tu sistema operativo con una interfaz animada y controles personalizados.

![SettingsPanel Demo](assets/splash.png)

## ✨ Características

- **🎨 Interfaz Animada**: Partículas dinámicas y efectos visuales suaves
- **🌍 Soporte Multiidioma**: Español e inglés (fácilmente extensible)
- **🎯 Detección Automática**: Reconocimiento inteligente de Windows/Linux
- **⚡ Optimizaciones Reales**: Comandos efectivos para mejorar el rendimiento
- **🌙 Modo Oscuro/Claro**: Interfaz adaptable con persistencia de configuraciones
- **🔧 Controles Personalizados**: Checkboxes, botones y terminal con estilo único

## 🚀 Instalación Rápida

### Prerrequisitos
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Windows
# Descargar Python desde https://python.org
```

### Instalación
```bash
# Clonar o descargar el proyecto
git clone https://github.com/JesusQuijada34/settingspanel.git
cd settingspanel

# Instalar dependencias
pip install -r lib/requirements.txt

# Ejecutar
python settingspanel.py
```

## 📦 requirements.txt
```txt
pygame==2.5.2
```

## 🎮 Cómo Usar

1. **Selección de Idioma**: Al iniciar, elige entre español, inglés o etc.
2. **Configuración del Sistema**: 
   - Windows: Optimizaciones de rendimiento y privacidad
   - Linux: Configuración básica del sistema y mantenimiento
3. **Aplicar Cambios**: Revise y confirme las optimizaciones
4. **Ver Resultados**: Monitorice los cambios en el terminal integrado

## 🛠️ Personalización

### Añadir Nuevo Idioma
```python
# En la sección de traducciones, agregar:
"nuevo_idioma": {
    "title": "Título en nuevo idioma",
    "select_language": "Seleccionar idioma",
    # ... más traducciones
}
```

### Añadir Nuevos Comandos
```python
# En apply_settings(), agregar:
if self.nuevo_checkbox.checked:
    commands.extend([
        'nuevo_comando_1',
        'nuevo_comando_2'
    ])
```

## 🎨 Personalización de Temas

### Modificar Colores
```python
# En la sección de temas:
GITHUB_LIGHT = {
    'bg': (246, 248, 250),        # Color de fondo
    'primary': (3, 102, 214),     # Color primario
    'success': (40, 167, 69),     # Color de éxito
    # ... más colores
}
```

### Añadir Nuevas Animaciones
```python
# En la clase Particle:
def update(self):
    # Modificar comportamiento de partículas
    self.x += self.speed_x * 0.95  # Efecto de desaceleración
    self.y += self.speed_y * 0.95
```

## 📋 Funcionalidades por Sistema

### 🪟 Windows
- ✅ Desactivar animaciones innecesarias
- ✅ Optimizar configuración Prefetch
- ✅ Desactivar sugerencias de Windows
- ✅ Limitar telemetría
- ✅ Desactivar publicidad integrada

### 🐧 Linux
- ✅ Activar firewall (UFW)
- ✅ Instalar actualizaciones disponibles
- ✅ Limpiar paquetes innecesarios

## 🚨 Precauciones

- ⚠️ Algunos cambios requieren permisos de administrador
- ⚠️ Siempre revise los comandos antes de ejecutar
- ⚠️ Haga backup de su sistema antes de cambios importantes

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Distribuido bajo licencia MIT. Ver `LICENSE` para más información.

## 🆘 Soporte

Si encuentras algún problema:
1. Revisa los issues existentes
2. Crea un nuevo issue con detalles del error
3. Proporciona información de tu sistema operativo

## 🏆 Créditos

**SettingsPanel** - Desarrollado con ❤️ para la comunidad de código abierto.

