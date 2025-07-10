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
        current_y = 30
        current_x = 26
        space = 70

        self.title_label = self.create.label("Настройки", font_size=36, bold=True, x=current_x, y=30, w=750, h=60)
        current_y += space

        self.fullscreen_checkbox = self.create.checkbox("Полноэкранный режим",checked=self.parent.settings.get("fullscreen", False),callback=self.toggle_fullscreen,x=current_x,y=current_y,w=300)
        current_y += 40

        self.volume_slider = self.create.slider("Громкость музыки", min_value=0, max_value=100,value=self.parent.settings.get("music_volume", 50),callback=self.update_music_volume, x=current_x, y=current_y, w=1000)
        current_y += space

        self.volume_slider = self.create.slider("Громкость звуков", min_value=0, max_value=100,value=self.parent.settings.get("effects_volume", 50),callback=self.update_effects_volume, x=current_x, y=current_y, w=1000)
        current_y += space

        self.fps_toggle = self.create.checkbox("Отображение фпс",checked=self.parent.settings.get("show_fps", False),callback=self.toggle_fps,x=current_x,y=current_y,w=500)
        current_y += space

        self.separator_line = self.create.separator(x=current_x,y=current_y,w=1000,h=10,color="rgba(255, 255, 255, 50)")

        self.close_button = self.create.button("Закрыть", self.close_settings, x=150, y=500, w=750, h=55, preset=2)

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