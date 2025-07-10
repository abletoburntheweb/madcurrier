from PyQt5.QtWidgets import QPushButton, QLabel, QCheckBox, QSlider, QFrame
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class Create:
    def __init__(self, parent):
        self.parent = parent

    def bc_image(label, pixmap, size):
        scaled_pixmap = pixmap.scaled(size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
        label.resize(size)
        label.show()

    def button(self, text, callback, x, y, w, h, bold=False, font_family="Montserrat", preset=1):
        button = QPushButton(text, self.parent)
        font = QFont(font_family, 20)
        if bold:
            font.setBold(True)
        button.setFont(font)
        button.clicked.connect(lambda: self.callback(callback))
        button.setGeometry(x, y, w, h)
        if preset == 1:
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
        elif preset == 2:
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: rgba(255, 255, 255, 20);
                    border: 2px solid white;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 40);
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
        label.setStyleSheet("""
            color: white;
            background-color: transparent;
        """) # Тут добавился прозрачный фон, чтобы в настройках и в паузе не было фона у текста
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

    def slider(self, text, min_value=0, max_value=100, value=50, bold=False, callback=None, x=0, y=0, w=600, h=30, font_family="Montserrat",):
        label = QLabel(text, self.parent)
        font = QFont(font_family, 18)
        if bold:
            font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: white; background-color: transparent;")
        label.setGeometry(x, y, w, h)

        slider = QSlider(Qt.Horizontal, self.parent)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(value)
        slider.setGeometry(x, y+40, w, 20)

        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background-color: rgba(255, 255, 255, 50);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                margin: -6px 0;
                background-color: white;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background-color: rgba(255, 255, 255, 150);
                border-radius: 4px;
            }
        """)

        if callback:
            slider.valueChanged.connect(callback)

        return label, slider

    def checkbox(self, text, checked=False, bold=False, callback=None, x=0, y=0, w=250, h=30, font_family="Montserrat",):
        checkbox = QCheckBox(text, self.parent)
        font = QFont(font_family, 18)
        if bold:
            font.setBold(True)
        checkbox.setFont(font)
        checkbox.setChecked(checked)
        checkbox.setGeometry(x, y, w, h)

        checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                background-color: transparent;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid white;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 20);
            }
            QCheckBox::indicator:checked {
                background-color: black;
                border: 2px solid white;
            }
            QCheckBox::indicator:!checked {
                background-color: white;
                border: 2px solid white;
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(255, 255, 255, 150);
            }
        """)

        if callback:
            checkbox.stateChanged.connect(lambda state: callback(state))

        return checkbox

    def separator(self, x=0, y=0, w=600, h=20, color="rgba(255, 255, 255, 50)"):
        line = QFrame(self.parent)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"color: {color};")
        line.setGeometry(x, y, w, h)
        return line

    def callback(self, callback):
        if hasattr(self.parent, "parent") and self.parent.parent:
            if callback.__name__ in ("open_settings", "open_leaderboard"):
                self.parent.parent.play_select_sound()
            elif callback.__name__ == "exit_game":
                self.parent.parent.play_cancel_sound()
            else:
                self.parent.parent.play_select_sound()
        callback()