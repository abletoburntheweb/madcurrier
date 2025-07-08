from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class Create:
    def __init__(self, parent):
        self.parent = parent


    def bc_image(self, path, parent=None):
        label = QLabel(parent or self.parent)
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Ошибка загрузки изображения: {path}")
        else:
            label.setPixmap(pixmap.scaled(label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        return label

    def button(self, text, callback, x, y, w, h, font_family="Montserrat"):
        button = QPushButton(text, self.parent)
        button.setFont(QFont(font_family, 20))
        button.clicked.connect(lambda: self.callback(callback))
        button.setGeometry(x, y, w, h)
        button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 black, stop:1 transparent);
                color: white;
                border: none;
                padding-left: 10px;
                font-size: 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 darkgray, stop:1 transparent);
            }
        """)
        return button

    def vert_buttons(self, buttons_data, s_x=0, s_y=0, spacing=80):
        buttons = []
        current_y = s_y

        for item in buttons_data:
            text = item['text']
            callback = item['callback']

            w = item.get('w', 750)
            h = item.get('h', 55)
            x = item.get('x', s_x)
            y = item.get('y', current_y)

            btn = self.button(text=text, callback=callback, x=x, y=y, w=w, h=h)
            buttons.append(btn)

            current_y = y + spacing

        return buttons

    def label(self, text, font_size=18, bold=False, x=0, y=0, w=200, h=50, font_family="Montserrat"):
        label = QLabel(text, self.parent)
        font = QFont(font_family, font_size)
        if bold:
            font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setGeometry(x, y, w, h)
        return label

    def ver_label(self, version="unknown", x=20, y=None, w=100, h=30, font_size=14, font_family="Montserrat"):
        text = f"ver{version}"
        label = QLabel(text, self.parent)
        font = QFont(font_family, font_size)
        label.setFont(font)
        label.setStyleSheet("color: white;")
        if y is None:
            y = self.parent.height() - h - 10
        label.setGeometry(x, y, w, h)
        return label

    def g_panel(self, x=0, y=0, w=800, h=1080):
        label = QLabel(self.parent)
        label.setGeometry(x, y, w, h)
        label.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 rgba(0,0,0,250), stop:1 rgba(0,0,0,40));
        """)
        return label


    def callback(self, callback):
        if hasattr(self.parent, "parent") and self.parent.parent:
            if callback.__name__ in ("open_settings", "open_leaderboard"):
                self.parent.parent.play_select_sound()
            elif callback.__name__ == "exit_game":
                self.parent.parent.play_cancel_sound()
            else:
                self.parent.parent.play_select_sound()
        callback()