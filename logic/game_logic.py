# engine/screens/game_logic.py
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QStackedWidget, QApplication
from PyQt5.QtCore import Qt, QUrl

from logic.creation import Create

from screens.settings_menu import SettingsMenu
from screens.main_menu import MainMenu

import json




class GameEngine(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.settings_file = "config/settings.json"
        self.settings = self.load_settings()

        # Инициализация медиа-плеера для музыки
        self.media_player = QMediaPlayer()
        self.current_music = None

        # Загрузка путей к музыке
        self.menu_music_path = "assets/audio/Niamos!.mp3"
        self.game_music_path = "assets/audio/game_music.mp3"
        self.intro_music_path = "assets/audio/intro_music.mp3"
        self.intro_music_volume = 50

        # Установка начальной громкости для музыки
        initial_volume = self.settings.get("music_volume", 50)
        self.media_player.setVolume(initial_volume)

        # Пути к звуковым эффектам
        self.select_sound_path = "assets/audio/select_click.mp3"
        self.cancel_sound_path = "assets/audio/cancel_click.mp3"

        # Инициализация медиаплеера для звуковых эффектов
        self.sound_player = QMediaPlayer()  # Создаем sound_player

        # Установка начальной громкости для звуковых эффектов
        initial_effects_volume = self.settings.get("effects_volume", 80)
        self.sound_player.setVolume(initial_effects_volume)  # Теперь это работает

        # Подключение сигналов
        self.currentChanged.connect(self.on_screen_changed)

        # Инициализация экранов
        self.init_screens()



    def init_screens(self):

        self.main_menu = MainMenu(self)
        self.addWidget(self.main_menu)

        self.settings_menu = SettingsMenu(self)
        self.addWidget(self.settings_menu)

        if self.settings.get("fullscreen", False):
            self.set_fullscreen(True)
        else:
            self.set_fullscreen(False)

        self.setCurrentWidget(self.main_menu)

    def load_settings(self):
        default_settings = {
            "fullscreen": False,
            "music_volume": 50,
            "effects_volume": 80  # Добавляем значение по умолчанию для громкости звуковых эффектов
        }
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                settings.setdefault("music_volume", 50)
                settings.setdefault("effects_volume", 80)  # Устанавливаем значение по умолчанию
                return settings
        except (json.JSONDecodeError, FileNotFoundError):
            print("Ошибка загрузки настроек. Используются настройки по умолчанию.")
        return default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def play_select_sound(self):
        try:
            print("Воспроизведение звука select_click...")
            media_content = QMediaContent(QUrl.fromLocalFile(self.select_sound_path))
            self.sound_player.setMedia(media_content)
            self.sound_player.play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука select_click: {e}")

    def play_cancel_sound(self):
        try:
            print("Воспроизведение звука cancel_click...")
            media_content = QMediaContent(QUrl.fromLocalFile(self.cancel_sound_path))
            self.sound_player.setMedia(media_content)
            self.sound_player.play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука cancel_click: {e}")

    def play_intro_music(self):
        print("Воспроизведение музыки интро...")
        self.stop_music()  # Останавливаем любую текущую музыку
        self.play_music(self.intro_music_path, loop=False)  # Запускаем intro_music без цикла
        self.media_player.setVolume(self.intro_music_volume)

    def stop_intro_music(self):
        print("Остановка музыки интро...")
        if self.current_music == self.intro_music_path:
            self.stop_music()

    def play_music(self, music_path, loop=True):
        try:
            print(f"Попытка воспроизвести музыку: {music_path}")
            if self.current_music == music_path and self.media_player.state() == QMediaPlayer.PlayingState:
                print("Музыка уже играет. Ничего не делаем.")
                return

            self.media_player.stop()

            try:
                print("Отключение предыдущих сигналов...")
                self.media_player.mediaStatusChanged.disconnect()
            except TypeError:
                print("Нет предыдущих сигналов для отключения.")
                pass

            self.current_music = music_path
            media_content = QMediaContent(QUrl.fromLocalFile(music_path))
            self.media_player.setMedia(media_content)

            if loop:
                print("Подключение сигнала циклического воспроизведения...")
                self.media_player.mediaStatusChanged.connect(self.loop_music)

            # Устанавливаем громкость из настроек
            self.media_player.setVolume(self.settings.get("music_volume", 50))

            # Всегда переходим в начало трека
            self.media_player.setPosition(0)
            print("Запуск воспроизведения...")
            self.media_player.play()

        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {e}")

    def loop_music(self, status):
        # Когда трек заканчивается, начинаем его снова
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def stop_music(self):
        try:
            self.media_player.stop()
            try:
                self.media_player.mediaStatusChanged.disconnect()
            except TypeError:
                pass  # Нет существующих соединений
            self.current_music = None
        except Exception as e:
            print(f"Ошибка остановки музыки: {e}")

    def on_screen_changed(self, index):
        current_widget = self.widget(index)
        if isinstance(current_widget, MainMenu):
            if not current_widget.is_intro_finished:
                print("Интро еще не завершено. Музыка главного меню не запускается.")
                return
            if self.current_music != self.menu_music_path:
                print("Переключение на музыку главного меню...")
                self.stop_music()
                self.play_music(self.menu_music_path)
            else:
                print("Музыка главного меню уже играет.")
        elif isinstance(current_widget, GameScreen) or isinstance(current_widget, GameScreenDuo):
            if self.current_music != self.game_music_path:
                print("Переключение на игровую музыку...")
                self.stop_music()
                self.play_music(self.game_music_path)
            else:
                print("Игровая музыка уже играет.")
        if self.current_music == self.intro_music_path:
            self.stop_intro_music()

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
        if self.currentWidget() == self.game_screen:
            self.game_screen.toggle_pause()

    def exit_game(self):
        self.media_player.stop()
        self.close()

    @staticmethod
    def interpolate_color(color1, color2, factor):
        r = int(color1.red() + (color2.red() - color1.red()) * factor)
        g = int(color1.green() + (color2.green() - color1.green()) * factor)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * factor)
        return QColor(r, g, b)
