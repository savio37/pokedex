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
        self.layout_frame.setSpacing(0)
        self.setLayout(self.layout_frame)
    
        self.pokemon = None
        
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
        
        label = QLabel("Height")
        label.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt;""")
        self.label_height = QLabel()
        self.label_height.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt; font-weight: normal;""")
        self.layout_frame.addWidget(label, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.layout_frame.addWidget(self.label_height, 3, 2, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        label = QLabel("Weight")
        label.setStyleSheet(f"""font-size: {DefaultFont.SIZE+4}pt;""")
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
        