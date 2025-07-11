# engine/screens/game_logic.py
import json

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt

from logic.creation import Create
from logic.music_manager import MusicManager

from screens.settings_menu import SettingsMenu
from screens.main_menu import MainMenu


class GameEngine(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Настройки игры
        self.settings_file = "config/settings.json"
        self.settings = self.load_settings()

        # Инициализация MusicManager
        self.music_manager = MusicManager()

        # Подключение сигналов
        self.currentChanged.connect(self.on_screen_changed)

        # Инициализация экранов
        self.init_screens()

    def init_screens(self):
        # Создание экранов
        self.main_menu = MainMenu(self)
        self.addWidget(self.main_menu)

        self.settings_menu = SettingsMenu(self)
        self.addWidget(self.settings_menu)

        # Установка полноэкранного режима
        if self.settings.get("fullscreen", False):
            self.set_fullscreen(True)
        else:
            self.set_fullscreen(False)

        # Устанавливаем главный экран
        self.setCurrentWidget(self.main_menu)

    def load_settings(self):
        # Загрузка настроек из файла
        default_settings = {
            "fullscreen": False,
        }
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                return settings
        except (json.JSONDecodeError, FileNotFoundError):
            print("Ошибка загрузки настроек. Используются настройки по умолчанию.")
            return default_settings

    def save_settings(self):
        # Сохранение настроек в файл
        try:
            with open(self.settings_file, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def on_screen_changed(self, index):
        # Обработка переключения экранов
        current_widget = self.widget(index)
        if isinstance(current_widget, MainMenu):
            if not current_widget.is_intro_finished:
                print("Интро еще не завершено. Музыка главного меню не запускается.")
                return
            self.music_manager.play_music(self.music_manager.menu_music_path)
        elif isinstance(current_widget, GameScreen) or isinstance(current_widget, GameScreenDuo):
            self.music_manager.play_music(self.music_manager.game_music_path)

    def toggle_fullscreen(self):
        # Переключение полноэкранного режима
        if self.isFullScreen():
            self.set_fullscreen(False)
        else:
            self.set_fullscreen(True)

    def set_fullscreen(self, fullscreen):
        # Установка полноэкранного режима
        if fullscreen:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.showFullScreen()
            self.settings["fullscreen"] = True
        else:
            self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            self.showNormal()
            self.settings["fullscreen"] = False
        self.save_settings()

    def toggle_pause(self):
        # Переключение паузы
        current_widget = self.currentWidget()
        if hasattr(current_widget, "toggle_pause"):
            current_widget.toggle_pause()

    def exit_game(self):
        # Выход из игры
        self.music_manager.stop_music()
        self.close()

    @staticmethod
    def interpolate_color(color1, color2, factor):
        # Интерполяция цветов
        r = int(color1.red() + (color2.red() - color1.red()) * factor)
        g = int(color1.green() + (color2.green() - color1.green()) * factor)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * factor)
        return QColor(r, g, b)