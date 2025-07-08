from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from screens.settings_menu import SettingsMenu
from logic.creation import Create


class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.overlay = None
        self.settings_menu = None
        self.leaderboard_widget = None
        self.current_modal_widget = None
        self.is_leaderboard_open = False
        self.is_settings_open = False
        self.current_mode = None
        self.background_pixmap = QPixmap("assets/textures/town.png")
        self.logo_pixmap = QPixmap("assets/textures/logo2.png")
        self.b_x = 25
        self.b_y = 450
        self.logo_label = None
        self.background_label = QLabel(self)
        self.is_intro_finished = False

        # Загрузка шрифтов
        self.c_font_l = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/sonic-hud-c-italic.ttf"))[0]
        self.c_font_b = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont("assets/font/MUNRO-sharedassets0.assets-232.otf"))[0]

        self.create = Create(self)

        self.init_ui()
        self.init_intro()

    def init_ui(self):
        self.setFixedSize(1920, 1080)

        self.gradient_label = self.create.g_panel()

        self.title_label = self.create.label("mad currier", font_size=66, bold=True, x=26, y=220, w=750, h=150, font_family=self.c_font_l)

        self.create.ver_label(version="99.99.99", font_family=self.c_font_b)

        self.start_button = self.create.button("Начать игру", self.start_game, x=self.b_x, y=self.b_y, w=750, h=55, font_family=self.c_font_b)
        self.start_duo_button = self.create.button("Играть вдвоем", self.start_duo, x=self.b_x, y=self.b_y + 80, w=750, h=55, font_family=self.c_font_b)
        self.leaderboard_button = self.create.button("Таблица рекордов", self.open_leaderboard, x=self.b_x, y=self.b_y + 160, w=750, h=55, font_family=self.c_font_b)
        self.settings_button = self.create.button("Настройки", self.open_settings, x=self.b_x, y=self.b_y + 240, w=750, h=55, font_family=self.c_font_b)
        self.exit_button = self.create.button("Выход", self.exit_game, x=self.b_x, y=self.b_y + 320, w=750, h=55, font_family=self.c_font_b)

        self.widgets_to_restore = [
            self.background_label,
            self.gradient_label,
            self.title_label,
            self.start_button,
            self.start_duo_button,
            self.leaderboard_button,
            self.settings_button,
            self.exit_button
        ]

        for widget in self.widgets_to_restore:
            widget.setProperty("original_pos", widget.pos())
            widget.hide()

    def init_intro(self):
        self.logo_label = QLabel(self)
        if self.logo_pixmap.isNull():
            print("Ошибка: не удалось загрузить файл assets/textures/logo2.png")
        else:
            self.logo_label.setPixmap(
                self.logo_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.logo_label.setGeometry(0, 0, self.width(), self.height())
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.show()
            self.fade(self.logo_label, duration=1500)
        QTimer.singleShot(10, lambda: self.parent.play_intro_music())
        QTimer.singleShot(4500, self.finish_intro)

    def finish_intro(self):
        self.show_background = True
        self.background_label.setPixmap(
            self.background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.background_label.show()
        if self.logo_label:
            self.logo_label.hide()
            self.logo_label.deleteLater()
            self.logo_label = None
        for widget in self.widgets_to_restore:
            widget.show()
            self.fade(widget, duration=600)
        if self.parent:
            self.parent.stop_intro_music()
        self.is_intro_finished = True
        QTimer.singleShot(500, lambda: self.parent.play_music(self.parent.menu_music_path))

    def fade(self, widget, duration=600):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()
        widget.animation = animation

    def start_game(self):
        pass

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
        pass

    def open_leaderboard(self):
        pass

    def open_settings(self):
        if self.is_settings_open:
            if self.parent:
                self.parent.play_cancel_sound()
            self.close_settings()
            return
        if self.parent:
            self.parent.play_select_sound()
        self.close_leaderboard()
        if not self.overlay:
            self.overlay = QWidget(self)
            self.overlay.setGeometry(800, 0, 1120, 1080)
            self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
            self.overlay.hide()
        if not self.settings_menu:
            self.settings_menu = SettingsMenu(parent=self.parent)
            self.settings_menu.setParent(self.overlay)
            self.settings_menu.move(50, 240)
            self.settings_menu.setFixedSize(1020, 600)
        self.overlay.show()
        self.settings_menu.show()
        self.is_settings_open = True

    def close_leaderboard(self):
        pass

    def close_settings(self):
        if self.settings_menu:
            self.settings_menu.hide()
        if self.overlay:
            self.overlay.hide()
        self.is_settings_open = False

    def exit_game(self):
        if self.parent:
            self.parent.exit_game()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.is_leaderboard_open:
                self.close_leaderboard()
                self.parent.play_cancel_sound()
            elif self.is_settings_open:
                self.close_settings()
                self.parent.play_cancel_sound()

    def disable_buttons(self):
        for btn in [self.start_button, self.start_duo_button, self.leaderboard_button, self.settings_button, self.exit_button]:
            btn.setDisabled(True)

    def enable_buttons(self):
        for btn in [self.start_button, self.start_duo_button, self.leaderboard_button, self.settings_button, self.exit_button]:
            btn.setDisabled(False)