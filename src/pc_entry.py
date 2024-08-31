from src.tools.ui_bricks import *

class AppWindowEntry(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 240)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet(DefaultStyle.APP_WINDOW)
        self.setFixedSize(700, 700)
        
        self.layout_window = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_window.setContentsMargins(0, 0, 0, 0)
        self.layout_window.setSpacing(0)
        self.setLayout(self.layout_window)
        
        titlebar = AppTitlebar(self)
        self.layout_window.addWidget(titlebar)
        
        self.layout_content = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_window.setContentsMargins(0, 0, 0, 0)
        self.layout_window.setSpacing(0)
        self.layout_window.addLayout(self.layout_content)
        
        border = QFrame()
        border.setFixedWidth(5)
        self.layout_content.addWidget(border)
        
        self.form = AppFormEntry(self)
        self.layout_content.addWidget(self.form)
        
        border = QFrame()
        border.setFixedWidth(5)
        self.layout_content.addWidget(border)
        
        border = QFrame()
        border.setFixedHeight(5)
        self.layout_window.addWidget(border)
        
        
class AppTitlebar(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFixedHeight(30)
        
        self.setMouseTracking(True)
        self.mouse_pos = None
        
        self.layout_titlebar = QBoxLayout(QBoxLayout.Direction.RightToLeft)
        self.layout_titlebar.setContentsMargins(0, 0, 0, 0)
        self.layout_titlebar.setSpacing(0)
        self.layout_titlebar.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout_titlebar)
        
        self.button_close = AppTitlebarButton()
        self.button_close.setIcon(Icon.CLOSE)
        self.button_close.setClicked(self.button_close_clicked)
        self.layout_titlebar.addWidget(self.button_close)
        
        self.button_minimize = AppTitlebarButton()
        self.button_minimize.setIcon(Icon.MINIMIZE)
        self.button_minimize.setClicked(self.button_minimize_clicked)
        self.layout_titlebar.addWidget(self.button_minimize)
        
    def button_minimize_clicked(self):
        self.window().showMinimized()
        
    def button_close_clicked(self):
        self.window().close()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pos = event.position().toPoint()
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.mouse_pos is not None:
            delta = event.position().toPoint() - self.mouse_pos
            self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.mouse_pos = None
        super().mouseReleaseEvent(event)
        
        
class AppFormEntry(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_frame = QGridLayout()
        self.layout_frame.setContentsMargins(15, 15, 15, 15)
        self.layout_frame.setSpacing(10)
        self.setLayout(self.layout_frame)
    
        self.pokemon = None
        
        self.button_delete = AppButton()
        self.button_delete.setIcon(Icon.DELETE)
        self.button_delete.setFixedSize(40, 40)
        self.button_delete.setStyleSheet(f"border-radius: 20px; background-color: {DefaultColor.BG_LIGHT};")
        self.button_delete.setClicked(self.button_delete_clicked)
        self.layout_frame.addWidget(self.button_delete, 0, 3, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        self.label_nickname = QLabel()
        self.label_nickname.setStyleSheet(f"""font-size: {DefaultFont.SIZE+6}pt;""")
        
        self.label_name = QLabel()
        self.label_name.setStyleSheet(f"""font-size: {DefaultFont.SIZE+6}pt;""")
        
        self.img_pokemon = AppImage()
        self.img_pokemon.setFixedSize(256, 256)
        self.layout_frame.addWidget(self.img_pokemon, 1, 0, 4, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.bar_level = AppXpBar()
        self.bar_level.setStyleSheet(f"""QProgressBar::chunk {{background-color: #00c954;}}""")
        self.layout_frame.addWidget(self.bar_level, 1, 2, 1, 2)
        
        self.img_type_1 = AppImage()
        self.img_type_1.setFixedSize(152, 36)
        
        self.img_type_2 = AppImage()
        self.img_type_2.setFixedSize(152, 36)
        
        label = AppEntryLabel("Height")
        self.label_height = QLabel()
        self.label_height.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt; font-weight: normal;""")
        self.layout_frame.addWidget(label, 3, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.label_height, 4, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        label = AppEntryLabel("Weight")
        self.label_weight = QLabel()
        self.label_weight.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt; font-weight: normal;""")
        self.layout_frame.addWidget(label, 3, 3, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.label_weight, 4, 3, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        label = AppEntryLabel("HP")
        self.bar_hp = AppStatBar()
        self.bar_hp.setStyleSheet(f"""QProgressBar::chunk {{background-color: #9EE865;}}""")
        self.layout_frame.addWidget(label, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_hp, 5, 1, 1, 3)
        
        label = AppEntryLabel("Atk")
        self.bar_atk = AppStatBar()
        self.bar_atk.setStyleSheet(f"""QProgressBar::chunk {{background-color: #F5DE69;}}""")
        self.layout_frame.addWidget(label, 6, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_atk, 6, 1, 1, 3)
        
        label = AppEntryLabel("Def")
        self.bar_def = AppStatBar()
        self.bar_def.setStyleSheet(f"""QProgressBar::chunk {{background-color: #F09A65;}}""")
        self.layout_frame.addWidget(label, 7, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_def, 7, 1, 1, 3)
        
        label = AppEntryLabel("SpAtk")
        self.bar_spatk = AppStatBar()
        self.bar_spatk.setStyleSheet(f"""QProgressBar::chunk {{background-color: #66D8F6;}}""")
        self.layout_frame.addWidget(label, 8, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spatk, 8, 1, 1, 3)
        
        label = AppEntryLabel("SpDef")
        self.bar_spdef = AppStatBar()
        self.bar_spdef.setStyleSheet(f"""QProgressBar::chunk {{background-color: #899EEA;}}""")
        self.layout_frame.addWidget(label, 9, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spdef, 9, 1, 1, 3)
        
        label = AppEntryLabel("Spd")
        self.bar_spd = AppStatBar()
        self.bar_spd.setStyleSheet(f"""QProgressBar::chunk {{background-color: #E46CCA;}}""")
        self.layout_frame.addWidget(label, 10, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spd, 10, 1, 1, 3)
        
        
    def set_pokemon(self, pokemon: dict):
        self.pokemon = pokemon
        if 'nickname' in pokemon:
            self.label_nickname.setText(pokemon['nickname'])
            self.label_name.setText(f"({pokemon['name']})")
            self.layout_frame.addWidget(self.label_nickname, 0, 0, 1, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            self.layout_frame.addWidget(self.label_name, 0, 2, 1, 2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        else:
            self.label_name.setText(pokemon['name'])
            self.layout_frame.addWidget(self.label_name, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.img_pokemon.setImage(pokemon['img'])
        self.img_type_1.setImage(pokemon['types'][0]['img'])
        if len(pokemon['types']) > 1:
            self.img_type_2.setImage(pokemon['types'][1]['img'])
            self.layout_frame.addWidget(self.img_type_1, 2, 2, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            self.layout_frame.addWidget(self.img_type_2, 2, 3, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        else:
            self.layout_frame.addWidget(self.img_type_1, 2, 2, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            
        self.label_height.setText(f"{pokemon['height']} m")
        self.label_weight.setText(f"{pokemon['weight']} kg")
        
        self.bar_level.setLevel(pokemon['level'])
        self.bar_level.setValue(pokemon['xp'])
        
        self.bar_hp.setValue(pokemon['stats']['hp'])
        self.bar_atk.setValue(pokemon['stats']['atk'])
        self.bar_def.setValue(pokemon['stats']['def'])
        self.bar_spatk.setValue(pokemon['stats']['spatk'])
        self.bar_spdef.setValue(pokemon['stats']['spdef'])
        self.bar_spd.setValue(pokemon['stats']['spd'])
        
    def button_delete_clicked(self):
        db.del_pokemon(self.pokemon['id'])
        self.window().close()


class AppEntryLabel(QLabel):
    def __init__(self, text:str | None = None):
        super().__init__(text)
        self.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt;""")        
    
    
class AppStatBar(QFrame):
    def __init__(self):
        super().__init__()
        self.layout_frame = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_frame.setContentsMargins(0, 0, 0, 0)
        self.layout_frame.setSpacing(0)
        self.setLayout(self.layout_frame)
        
        self.button_minus = AppButton()
        self.button_minus.setText("-")
        self.button_minus.setFixedSize(24, 38)
        self.button_minus.setStyleSheet("border-top-left-radius: 5px; border-bottom-left-radius: 5px;")
        self.button_minus.setClicked(self.button_minus_clicked)
        self.layout_frame.addWidget(self.button_minus)
        
        self.bar = QProgressBar()
        self.bar.setFormat("%v")
        self.bar.setMaximum(255)
        self.layout_frame.addWidget(self.bar)
        
        self.button_plus = AppButton()
        self.button_plus.setText("+")
        self.button_plus.setFixedSize(24, 38)
        self.button_plus.setStyleSheet("border-top-right-radius: 5px; border-bottom-right-radius: 5px;")
        self.button_plus.setClicked(self.button_plus_clicked)
        self.layout_frame.addWidget(self.button_plus)
        
    def button_minus_clicked(self):
        self.setValue(self.value() - 1)
        
    def button_plus_clicked(self):
        self.setValue(self.value() + 1)
        
    def value(self):
        return self.bar.value()
    
    def setValue(self, value: int):
        self.bar.setValue(value)
        
        
class AppXpBar(QFrame):
    def __init__(self):
        super().__init__()
        self.layout_frame = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_frame.setContentsMargins(0, 0, 0, 0)
        self.layout_frame.setSpacing(0)
        self.setLayout(self.layout_frame)
        
        self.level = 1
        
        self.button_down = AppButton()
        self.button_down.setText("▼")
        self.button_down.setFixedSize(24, 24)
        self.button_down.setStyleSheet("border-top-left-radius: 5px; border-bottom-left-radius: 5px;")
        self.button_down.setClicked(self.button_down_clicked)
        self.layout_frame.addWidget(self.button_down)
        
        self.button_minus = AppButton()
        self.button_minus.setText("-")
        self.button_minus.setFixedSize(24, 38)
        self.button_minus.setStyleSheet("border-top-left-radius: 5px; border-bottom-left-radius: 5px;")
        self.button_minus.setClicked(self.button_minus_clicked)
        self.layout_frame.addWidget(self.button_minus)
        
        self.bar = QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setFormat(f"{self.level} (%v XP)")
        self.layout_frame.addWidget(self.bar)
        
        self.button_plus = AppButton()
        self.button_plus.setText("+")
        self.button_plus.setFixedSize(24, 38)
        self.button_plus.setStyleSheet("border-top-right-radius: 5px; border-bottom-right-radius: 5px;")
        self.button_plus.setClicked(self.button_plus_clicked)
        self.layout_frame.addWidget(self.button_plus)
        
        self.button_up = AppButton()
        self.button_up.setText("▲")
        self.button_up.setFixedSize(24, 24)
        self.button_up.setStyleSheet("border-top-right-radius: 5px; border-bottom-right-radius: 5px;")
        self.button_up.setClicked(self.button_up_clicked)
        self.layout_frame.addWidget(self.button_up)
        
    def button_minus_clicked(self):
        self.setValue(self.value() - 1)
        
    def button_plus_clicked(self):
        self.setValue(self.value() + 1)
        
    def button_up_clicked(self):
        self.setLevel(self.level + 1)
        self.bar.setFormat(f"{self.level} (%v XP)")
        
    def button_down_clicked(self):
        if self.level > 1:
            self.setLevel(self.level - 1)
        self.bar.setFormat(f"{self.level} (%v XP)")
        
    def setLevel(self, level: int):
        self.level = level
        
    def value(self):
        return self.bar.value()
    
    def setValue(self, value: int):
        self.bar.setValue(value)