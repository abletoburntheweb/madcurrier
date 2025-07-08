from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame
from logic.creation import Create


class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create = Create(self)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title_label = self.create.label("Настройки", font_size=36, bold=True)
        layout.addWidget(title_label)

        self.fullscreen_toggle = self.create.checkbox("Полноэкранный режим", checked=self.parent.settings.get("fullscreen", False))
        self.fullscreen_toggle.stateChanged.connect(self.toggle_fullscreen)
        layout.addWidget(self.fullscreen_toggle)

        volume_label = self.create.label("Громкость музыки", font_size=18)
        layout.addWidget(volume_label)
        self.volume_slider = self.create.slider(value=self.parent.settings.get("music_volume", 50))
        self.volume_slider.valueChanged.connect(self.update_music_volume)
        layout.addWidget(self.volume_slider)

        effects_label = self.create.label("Громкость звуков", font_size=18)
        layout.addWidget(effects_label)
        self.effects_slider = self.create.slider(value=self.parent.settings.get("effects_volume", 80))
        self.effects_slider.valueChanged.connect(self.update_effects_volume)
        layout.addWidget(self.effects_slider)

        self.fps_toggle = self.create.checkbox("Отображать FPS", checked=self.parent.settings.get("show_fps", True))
        self.fps_toggle.stateChanged.connect(self.toggle_fps)
        layout.addWidget(self.fps_toggle)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: rgba(255, 255, 255, 50);")
        layout.addWidget(separator)

        self.close_button = self.create.transparent_button("Закрыть")
        self.close_button.clicked.connect(self.close_settings)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def toggle_fullscreen(self, state):
        if self.parent:
            self.parent.toggle_fullscreen()

    def update_music_volume(self, value):
        if self.parent:
            self.parent.media_player.setVolume(value)
            self.parent.settings["music_volume"] = value
            self.parent.save_settings()

    def update_effects_volume(self, value):
        if self.parent:
            self.parent.sound_player.setVolume(value)
            self.parent.settings["effects_volume"] = value
            self.parent.save_settings()

    def toggle_fps(self, state):
        if self.parent:
            self.parent.settings["show_fps"] = bool(state)
            self.parent.save_settings()
            if hasattr(self.parent.game_screen, "update_fps_visibility"):
                self.parent.game_screen.update_fps_visibility(bool(state))

    def close_settings(self):
        if self.parent:
            self.parent.main_menu.close_settings()
            self.parent.play_cancel_sound()