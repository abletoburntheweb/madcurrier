# engine/screens/game_logic.py

import json
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt
from logic.creation import Create
from logic.intro_animation import IntroAnimation
from logic.music_manager import MusicManager
from screens.game_screen import GameScreen
from screens.pause_menu import PauseMenu
from screens.settings_menu import SettingsMenu
from screens.main_menu import MainMenu
from logic.settings_manager import load_settings, save_settings

class GameEngine(QStackedWidget):
    def __init__(self):
        super().__init__()
        # Загрузка настроек
        self.settings = load_settings()

        # Инициализация MusicManager с текущими настройками
        self.music_manager = MusicManager(self.settings)

        # Подключение сигналов
        self.currentChanged.connect(self.on_screen_changed)

        # Инициализация экранов
        self.init_screens()

    def init_screens(self):
        self.main_menu = MainMenu(self)
        self.intro = IntroAnimation(parent=self, main_menu_widget=self.main_menu)
        self.addWidget(self.intro)
        self.addWidget(self.main_menu)
        self.settings_menu = SettingsMenu(self)
        self.addWidget(self.settings_menu)
        self.game_screen = GameScreen(parent=self)
        self.addWidget(self.game_screen)
        self.pause_menu = PauseMenu(parent=self)
        self.addWidget(self.pause_menu)

        # Установка полноэкранного режима
        if self.settings.get("fullscreen", False):
            self.set_fullscreen(True)
        else:
            self.set_fullscreen(False)

        # Устанавливаем главный экран
        self.setCurrentWidget(self.intro)

    def save_settings(self):
        save_settings(self.settings)

    def on_screen_changed(self, index):
        current_widget = self.widget(index)
        if isinstance(current_widget, MainMenu):
            if not current_widget.is_intro_finished:
                print("Интро еще не завершено. Музыка главного меню не запускается.")
                return
            self.music_manager.play_music(self.music_manager.menu_music)
        elif isinstance(current_widget, GameScreen):
            self.music_manager.play_music(self.music_manager.game_music)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.set_fullscreen(False)
        else:
            self.set_fullscreen(True)

    def set_fullscreen(self, fullscreen):
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
        current_widget = self.currentWidget()
        if hasattr(current_widget, "toggle_pause"):
            current_widget.toggle_pause()

    @staticmethod
    def interpolate_color(color1, color2, factor):
        r = int(color1.red() + (color2.red() - color1.red()) * factor)
        g = int(color1.green() + (color2.green() - color1.green()) * factor)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * factor)
        return QColor(r, g, b)