from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import json

class MusicManager:
    def __init__(self):
        self.menu_music_path = "assets/audio/Niamos!.mp3"
        self.game_music_path = "assets/audio/game_music.mp3"
        self.intro_music_path = "assets/audio/intro_music.mp3"
        self.select_sound_path = "assets/audio/select_click.mp3"
        self.cancel_sound_path = "assets/audio/cancel_click.mp3"

        self.settings_file = "config/settings.json"
        self.default_settings = {
            "music_volume": 50,
            "effects_volume": 80
        }
        self.settings = self.load_settings()

        # Инициализация медиаплееров
        self.music_player = QMediaPlayer()
        self.sfx_player = QMediaPlayer()

        # Установка начальной громкости
        self.set_music_volume(self.settings.get("music_volume", 50))
        self.set_sfx_volume(self.settings.get("effects_volume", 80))

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                settings.setdefault("music_volume", 50)
                settings.setdefault("effects_volume", 80)
                return settings
        except (json.JSONDecodeError, FileNotFoundError):
            print("Ошибка загрузки настроек. Используются настройки по умолчанию.")
            return self.default_settings

    def save_settings(self):
        try:
            with open(self.settings_file, "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def set_music_volume(self, volume):
        self.music_player.setVolume(volume)
        self.settings["music_volume"] = volume
        self.save_settings()

    def set_sfx_volume(self, volume):
        self.sfx_player.setVolume(volume)
        self.settings["effects_volume"] = volume
        self.save_settings()

    def play_music(self, music_path, loop=True):
        try:
            if self.music_player.currentMedia() and self.music_player.currentMedia().canonicalUrl().toString() == QUrl.fromLocalFile(music_path).toString():
                print("Музыка уже играет. Ничего не делаем.")
                return

            self.music_player.stop()
            media_content = QMediaContent(QUrl.fromLocalFile(music_path))
            self.music_player.setMedia(media_content)
            self.music_player.setPosition(0)

            if loop:
                self.music_player.mediaStatusChanged.connect(self.loop_music)

            self.music_player.play()
        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {e}")

    def loop_music(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.music_player.setPosition(0)
            self.music_player.play()

    def stop_music(self):
        try:
            self.music_player.stop()
            try:
                self.music_player.mediaStatusChanged.disconnect()
            except TypeError:
                pass
        except Exception as e:
            print(f"Ошибка остановки музыки: {e}")

    def play_sfx(self, sound_path):
        try:
            media_content = QMediaContent(QUrl.fromLocalFile(sound_path))
            self.sfx_player.setMedia(media_content)
            self.sfx_player.play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")

    def stop_sfx(self):
        try:
            self.sfx_player.stop()
        except Exception as e:
            print(f"Ошибка остановки звука: {e}")

    def play_select_sound(self):
        self.play_sfx(self.select_sound_path)

    def play_cancel_sound(self):
        self.play_sfx(self.cancel_sound_path)
