from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

from logic.music_manager import MusicManager
from logic.transitions import Transitions
from logic.creation import Create
from logic.settings_manager import load_settings, save_settings


class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.overlay = None
        self.settings_menu = None
        self.is_leaderboard_open = False
        self.is_settings_open = False

        self.settings = load_settings()

        self.b_x = 25
        self.b_y = 450
        self.is_intro_finished = False

        self.c_font_l = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/sonic-hud-c-italic.ttf"))[0]
        self.c_font_b = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/MUNRO-sharedassets0.assets-232.otf"))[0]

        self.create = Create(self)
        self.music_manager = self.parent.music_manager
        self.transitions = Transitions(self.parent)

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1920, 1080)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()


        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("assets/textures/town.png").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.gradient_label = self.create.g_panel()

        self.logo_pixmap = QPixmap("assets/textures/logo2.png")

        self.title_label = self.create.label("mad currier", font_size=66, bold=True, x=26, y=220, w=750, h=150, font_family=self.c_font_l)

        self.create.ver_label(version="99.99.99", font_family=self.c_font_b)

        self.start_button = self.create.button("Начать игру", self.start_game, x=self.b_x, y=self.b_y, w=750, h=55, font_family=self.c_font_b)
        self.start_duo_button = self.create.button("Играть вдвоем", self.start_duo, x=self.b_x, y=self.b_y + 80, w=750, h=55, font_family=self.c_font_b)
        self.leaderboard_button = self.create.button( "Таблица рекордов", self.open_leaderboard, x=self.b_x, y=self.b_y + 160, w=750, h=55, font_family=self.c_font_b)
        self.settings_button = self.create.button(
            "Настройки", self.transitions.open_settings, x=self.b_x, y=self.b_y + 240, w=750, h=55,
            font_family=self.c_font_b
        )
        self.exit_button = self.create.button("Выход", self.exit_game, x=self.b_x, y=self.b_y + 320, w=750, h=55, font_family=self.c_font_b)

        self.widgets_to_restore = [self.background_label,self.gradient_label,self.title_label,self.start_button, self.start_duo_button,self.leaderboard_button,self.settings_button,self.exit_button, ]

        for widget in self.widgets_to_restore:
            widget.setProperty("original_pos", widget.pos())

    def start_game(self):
        self.music_manager.play_select_sound()

    def restore_positions(self):
        self.gradient_label.move(0, 0)
        self.title_label.move(0, 220)
        b_x = 25
        b_y = 450
        self.start_button.move(b_x, b_y)
        self.start_duo_button.move(b_x, b_y + 80)
        self.leaderboard_button.move(b_x, b_y + 160)
        self.settings_button.move(b_x, b_y + 240)
        self.exit_button.move(b_x, b_y + 320)
        self.enable_buttons()

    def start_duo(self):
        self.music_manager.play_select_sound()

    def open_leaderboard(self):
        self.music_manager.play_select_sound()

    def close_leaderboard(self):
        self.music_manager.play_cancel_sound()

    def exit_game(self):
        self.music_manager.play_cancel_sound()
        if self.parent:
            self.parent.exit_game()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.is_leaderboard_open:
                self.close_leaderboard()
            elif self.is_settings_open:
                self.transitions.close_settings()

        if event.key() == Qt.Key_Space:
            if not self.is_intro_finished:
                self.finish_intro()

    def disable_buttons(self):
        for btn in [self.start_button, self.start_duo_button, self.leaderboard_button, self.settings_button, self.exit_button]:
            btn.setDisabled(True)

    def enable_buttons(self):
        for btn in [self.start_button, self.start_duo_button, self.leaderboard_button, self.settings_button, self.exit_button]:
            btn.setDisabled(False)
