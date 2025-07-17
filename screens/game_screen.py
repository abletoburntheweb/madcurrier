import random
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QRect

from logic.transitions import Transitions


class GameScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_game_variables()
        self.is_game_active = False
        self.transitions = Transitions(self.parent())
        self.start_timer()

    def init_ui(self):
        self.setFixedSize(1920, 1080)
        self.setFocusPolicy(Qt.StrongFocus)

    def init_game_variables(self):
        self.player_x = 960
        self.player_y = 900
        self.player_width = 50
        self.player_height = 50
        self.player_speed = 5
        self.car_width = 50
        self.car_height = 50
        self.car_speed = 5
        self.cars = []
        self.points = 0

    def start_game(self):
        """Запуск игры."""
        if not self.is_game_active:
            self.is_game_active = True
            self.init_game_variables()
            self.spawn_cars()
            self.timer.start()
            print("Игра началась!")
    def spawn_cars(self):
        for _ in range(5):
            x = random.randint(50, 1870)
            y = random.randint(-500, -50)
            direction = random.choice([-1, 1])
            self.cars.append({"x": x, "y": y, "direction": direction})
           # print(f"Создана машина: x={x}, y={y}, direction={direction}")

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

    def update_game(self):
        if not self.is_game_active:
            return

        self.move_player()
        self.move_cars()
        self.check_collisions()
        self.repaint()

    def move_player(self):
        keys = getattr(self, "keys", {})
        if keys.get(Qt.Key_A, False):
            self.player_x -= self.player_speed
            if self.player_x < 0:
                self.player_x = 0
        if keys.get(Qt.Key_D, False):
            self.player_x += self.player_speed
            if self.player_x > self.width() - self.player_width:
                self.player_x = self.width() - self.player_width

    def move_cars(self):
        for i in range(len(self.cars)):
            self.cars[i]["y"] += self.car_speed

            if self.cars[i]["y"] > self.height():
                self.cars[i]["y"] = random.randint(-500, -50)
                self.cars[i]["x"] = random.randint(50, 1870)

            elif self.cars[i]["y"] + self.car_height < 0:
                self.cars[i]["y"] = random.randint(self.height(), self.height() + 500)
                self.cars[i]["x"] = random.randint(50, 1870)

    def check_collisions(self):
        player_rect = QRect(self.player_x, self.player_y, self.player_width, self.player_height)
        for car in self.cars:
            car_rect = QRect(car["x"], car["y"], self.car_width, self.car_height)
            if player_rect.intersects(car_rect):
                self.game_over()

    def game_over(self):
        """Завершение игры."""
        self.timer.stop()
        reply = QMessageBox()
        reply.setIcon(QMessageBox.Information)
        reply.setWindowTitle("Game Over")
        reply.setText(f"Вы проиграли! Очки: {self.points}")
        retry_button = reply.addButton("Retry", QMessageBox.AcceptRole)
        cancel_button = reply.addButton("Cancel", QMessageBox.RejectRole)
        reply.setDefaultButton(retry_button)

        reply.exec_()

        if reply.clickedButton() == retry_button:
            self.restart_game()
        elif reply.clickedButton() == cancel_button:
            self.return_to_main_menu()

    def restart_game(self):
        self.init_game_variables()
        self.spawn_cars()
        self.timer.start()

    def return_to_main_menu(self):
        self.timer.stop()
        if self.transitions:
            self.transitions.close_game()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), QColor(255, 255, 255))

        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(self.player_x, self.player_y, self.player_width, self.player_height)

        painter.setBrush(QColor(255, 0, 0))
        for car in self.cars:
           # print(f"Отрисовка машины: x={car['x']}, y={car['y']}")
            painter.drawRect(car["x"], car["y"], self.car_width, self.car_height)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if not hasattr(self.parent(), "pause_menu"):
                from screens.pause_menu import PauseMenu
                self.parent().pause_menu = PauseMenu(parent=self.parent())
            self.timer.stop()
            self.parent().setCurrentWidget(self.parent().pause_menu)
            self.parent().pause_menu.show()
        else:
            self.keys = getattr(self, "keys", {})
            self.keys[event.key()] = True

    def keyReleaseEvent(self, event):
        self.keys = getattr(self, "keys", {})
        self.keys[event.key()] = False