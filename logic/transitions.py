# logic/transitions.py

from PyQt5.QtWidgets import QWidget


def transition_open_game(parent):
    if not hasattr(parent, "main_menu"):
        print("Ошибка: Родительский объект не содержит main_menu.")
        return

    main_menu = parent.main_menu

    if main_menu.is_game_open:
        transition_close_game(parent)
        return

    if hasattr(parent, "music_manager"):
        parent.music_manager.play_select_sound()

    # Ленивый импорт GameScreen
    from screens.game_screen import GameScreen
    parent.game_screen = GameScreen(parent=parent)  # Пересоздаем экран игры

    # Скрываем главное меню
    main_menu.hide()

    # Показываем игровой экран через GameEngine
    parent.addWidget(parent.game_screen)  # Добавляем новый экран в стек
    parent.setCurrentWidget(parent.game_screen)

    # Запускаем игру
    parent.game_screen.start_game()  # Вызываем метод start_game
    main_menu.is_game_open = True


def transition_close_game(parent):
    if not hasattr(parent, "main_menu"):
        print("Ошибка: Родительский объект не содержит main_menu.")
        return

    main_menu = parent.main_menu

    if not main_menu.is_game_open:
        return

    if hasattr(parent, "music_manager"):
        parent.music_manager.play_cancel_sound()

    # Удаляем текущий экран игры из стека
    if hasattr(parent, "game_screen") and parent.game_screen:
        parent.removeWidget(parent.game_screen)  # Удаляем старый экран игры

    # Возвращаемся в главное меню
    parent.setCurrentWidget(parent.main_menu)
    main_menu.show()
    main_menu.is_game_open = False


def transition_resume_game(parent):
    """Возобновление игры."""
    if not hasattr(parent, "game_screen"):
        print("Ошибка: Родительский объект не содержит game_screen.")
        return

    # Восстанавливаем игровой процесс
    parent.game_screen.timer.start()  # Возобновляем таймер игры
    parent.setCurrentWidget(parent.game_screen)  # Возвращаемся к игровому экрану
    parent.game_screen.repaint()  # Принудительное обновление экрана


def transition_exit_to_main_menu(parent):
    """Выход в главное меню."""
    if not hasattr(parent, "main_menu"):
        print("Ошибка: Родительский объект не содержит main_menu.")
        return

    main_menu = parent.main_menu

    # Останавливаем игру
    if hasattr(parent, "game_screen") and parent.game_screen:
        parent.game_screen.timer.stop()

    # Возвращаемся в главное меню
    parent.setCurrentWidget(main_menu)
    main_menu.show()
    main_menu.is_game_open = False


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


def transition_exit_game(parent):
    """Выход из игры."""
    if hasattr(parent, "music_manager"):
        parent.music_manager.stop_music()

    parent.close()


class Transitions:
    def __init__(self, parent):
        self.parent = parent

    def open_game(self):
        transition_open_game(self.parent)

    def close_game(self):
        transition_close_game(self.parent)

    def resume_game(self):
        transition_resume_game(self.parent)

    def exit_to_main_menu(self):
        transition_exit_to_main_menu(self.parent)

    def open_settings(self):
        transition_open_settings(self.parent)

    def close_settings(self):
        transition_close_settings(self.parent)

    def exit_game(self):
        transition_exit_game(self.parent)
