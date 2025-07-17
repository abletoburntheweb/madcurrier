from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtCore import Qt
from logic.transitions import Transitions
from logic.creation import Create


class PauseMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.overlay = None
        self.settings_menu = None
        self.is_settings_open = False
        self.is_pause_open = False

        self.settings = parent.settings if hasattr(parent, "settings") else {}

        self.b_x = 25
        self.b_y = 450

        self.c_font_l = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/sonic-hud-c-italic.ttf"))[0]
        self.c_font_b = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/MUNRO-sharedassets0.assets-232.otf"))[0]

        self.create = Create(self)
        self.transitions = Transitions(self.parent)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1920, 1080)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.background_label = QLabel(self)
        self.background_label.setPixmap(
            QPixmap("assets/textures/town.png").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        )

        self.gradient_label = self.create.g_panel()

        self.title_label = self.create.label(
            "Пауза", font_size=66, bold=True, x=26, y=220, w=750, h=150, font_family=self.c_font_l
        )

        self.resume_button = self.create.button("Продолжить", self.transitions.resume_game, x=self.b_x, y=self.b_y, w=750, h=55, font_family=self.c_font_b)
        self.settings_button = self.create.button("Настройки", self.transitions.open_settings, x=self.b_x, y=self.b_y + 80, w=750, h=55, font_family=self.c_font_b)
        self.exit_to_main_menu_button = self.create.button("Выйти в главное меню", self.transitions.exit_to_main_menu, x=self.b_x, y=self.b_y + 160, w=750, h=55, font_family=self.c_font_b)