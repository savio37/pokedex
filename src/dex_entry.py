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
        
        self.button_add = AppButton()
        self.button_add.setIcon(Icon.PC)
        self.button_add.setFixedSize(40, 40)
        self.button_add.setStyleSheet(f"border-radius: 20px; background-color: {DefaultColor.BG_LIGHT};")
        self.button_add.setClicked(self.add_to_pc)
        self.layout_frame.addWidget(self.button_add, 0, 3, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        self.label_num = QLabel()
        self.label_num.setStyleSheet(f"""font-size: {DefaultFont.SIZE+6}pt;""")
        self.layout_frame.addWidget(self.label_num, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.label_especie = QLabel()
        self.label_especie.setStyleSheet(f"""font-size: {DefaultFont.SIZE+6}pt;""")
        self.layout_frame.addWidget(self.label_especie, 0, 1, 1, 2, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        self.img_especie = AppImage()
        self.img_especie.setFixedSize(256, 256)
        self.layout_frame.addWidget(self.img_especie, 1, 0, 4, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.img_tipo_1 = AppImage()
        self.img_tipo_1.setFixedSize(152, 36)
        
        self.img_tipo_2 = AppImage()
        self.img_tipo_2.setFixedSize(152, 36)
        
        label = AppDexLabel("Height")
        self.label_height = QLabel()
        self.label_height.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt; font-weight: normal;""")
        self.layout_frame.addWidget(label, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.label_height, 3, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        label = AppDexLabel("Weight")
        self.label_weight = QLabel()
        self.label_weight.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt; font-weight: normal;""")
        self.layout_frame.addWidget(label, 2, 3, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.label_weight, 3, 3, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.label_desc = QLabel()
        self.label_desc.setStyleSheet(f"""font-size: {DefaultFont.SIZE+2}pt; font-weight: normal;""")
        self.label_desc.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.label_desc.setWordWrap(True)
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.layout_frame.addWidget(self.label_desc, 4, 2, 1, 2, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        label = AppDexLabel("HP")
        self.bar_hp = AppStatBar()
        self.bar_hp.setStyleSheet(f"""QProgressBar::chunk {{background-color: #9EE865;}}""")
        self.layout_frame.addWidget(label, 5, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_hp, 5, 1, 1, 3)
        
        label = AppDexLabel("Atk")
        self.bar_atk = AppStatBar()
        self.bar_atk.setStyleSheet(f"""QProgressBar::chunk {{background-color: #F5DE69;}}""")
        self.layout_frame.addWidget(label, 6, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_atk, 6, 1, 1, 3)
        
        label = AppDexLabel("Def")
        self.bar_def = AppStatBar()
        self.bar_def.setStyleSheet(f"""QProgressBar::chunk {{background-color: #F09A65;}}""")
        self.layout_frame.addWidget(label, 7, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_def, 7, 1, 1, 3)
        
        label = AppDexLabel("SpAtk")
        self.bar_spatk = AppStatBar()
        self.bar_spatk.setStyleSheet(f"""QProgressBar::chunk {{background-color: #66D8F6;}}""")
        self.layout_frame.addWidget(label, 8, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spatk, 8, 1, 1, 3)
        
        label = AppDexLabel("SpDef")
        self.bar_spdef = AppStatBar()
        self.bar_spdef.setStyleSheet(f"""QProgressBar::chunk {{background-color: #899EEA;}}""")
        self.layout_frame.addWidget(label, 9, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spdef, 9, 1, 1, 3)
        
        label = AppDexLabel("Spd")
        self.bar_spd = AppStatBar()
        self.bar_spd.setStyleSheet(f"""QProgressBar::chunk {{background-color: #E46CCA;}}""")
        self.layout_frame.addWidget(label, 10, 0, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.bar_spd, 10, 1, 1, 3)
        
        
    def set_species(self, species: dict):
        self.pokemon = species
        self.label_num.setText(f"#{species['id']:03}")
        self.label_especie.setText(species['name'])
        self.img_especie.setImage(species['img'])
        self.img_tipo_1.setImage(species['types'][0]['img'])
        if len(species['types']) > 1:
            self.img_tipo_2.setImage(species['types'][1]['img'])
            self.layout_frame.addWidget(self.img_tipo_1, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            self.layout_frame.addWidget(self.img_tipo_2, 1, 3, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        else:
            self.layout_frame.addWidget(self.img_tipo_1, 1, 2, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
            
        self.label_height.setText(f"{species['height']} m")
        self.label_weight.setText(f"{species['weight']} kg")
        self.label_desc.setText(species['description'])
        
        self.bar_hp.setValue(species['stats']['hp'])
        self.bar_atk.setValue(species['stats']['atk'])
        self.bar_def.setValue(species['stats']['def'])
        self.bar_spatk.setValue(species['stats']['spatk'])
        self.bar_spdef.setValue(species['stats']['spdef'])
        self.bar_spd.setValue(species['stats']['spd'])
        
    
    def add_to_pc(self):
        if self.pokemon is not None:
            new_pokemon = {}
            new_pokemon['name'] = self.pokemon['name']
            new_pokemon['img'] = self.pokemon['img']
            new_pokemon['types'] = self.pokemon['types']
            new_pokemon['height'] = self.pokemon['height']
            new_pokemon['weight'] = self.pokemon['weight']
            new_pokemon['stats'] = self.pokemon['stats']
            new_pokemon['level'] = 1
            new_pokemon['xp'] = 0
            db.add_pokemon(new_pokemon)

class AppDexLabel(QLabel):
    def __init__(self, text:str | None = None):
        super().__init__(text)
        self.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt;""")        
    
    
class AppStatBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setFormat("%v")
        self.setMaximum(255)