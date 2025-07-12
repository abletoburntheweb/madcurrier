# logic/transitions.py

from PyQt5.QtWidgets import QWidget


def transition_open_settings(parent):
    if not hasattr(parent, "main_menu"):
        print("Ошибка: Родительский объект не содержит main_menu.")
        return

    main_menu = parent.main_menu

    if main_menu.is_settings_open:
        transition_close_settings(parent)
        return

    if hasattr(parent, "music_manager"):
        parent.music_manager.play_select_sound()

    if not main_menu.overlay:
        main_menu.overlay = QWidget(main_menu)
        main_menu.overlay.setGeometry(800, 0, 1120, 1080)
        main_menu.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        main_menu.overlay.hide()

    if not main_menu.settings_menu:
        from screens.settings_menu import SettingsMenu
        main_menu.settings_menu = SettingsMenu(parent=parent)
        main_menu.settings_menu.setParent(main_menu.overlay)
        main_menu.settings_menu.move(50, 240)
        main_menu.settings_menu.setFixedSize(1020, 600)

    main_menu.overlay.show()
    main_menu.settings_menu.show()
    main_menu.is_settings_open = True


def transition_close_settings(parent):
    if not hasattr(parent, "main_menu"):
        print("Ошибка: Родительский объект не содержит main_menu.")
        return

    main_menu = parent.main_menu

    if not main_menu.is_settings_open:
        return

    if hasattr(parent, "music_manager"):
        parent.music_manager.play_cancel_sound()

    if main_menu.settings_menu:
        main_menu.settings_menu.hide()
    if main_menu.overlay:
        main_menu.overlay.hide()

    main_menu.is_settings_open = False


class Transitions:
    def __init__(self, parent):
        self.parent = parent

    def open_settings(self):
        transition_open_settings(self.parent)

    def close_settings(self):
        transition_close_settings(self.parent)
