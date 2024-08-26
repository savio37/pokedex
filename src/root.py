from src.tools.ui_bricks import *
from src.dex import AppFormDex
from src.types import AppFormTypes
from src.pc import AppFormPC

class AppWindowRoot(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1080, 720)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(DefaultStyle.APP_WINDOW)
        
        self.layout_window = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_window.setContentsMargins(0, 0, 0, 0)
        self.layout_window.setSpacing(0)
        self.setLayout(self.layout_window)
        
        titlebar = AppTitlebar(self)
        self.layout_window.addWidget(titlebar)
        
        self.layout_content = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_content.setContentsMargins(0, 0, 0, 0)
        self.layout_content.setSpacing(0)
        self.layout_window.addLayout(self.layout_content)
        
        border = QFrame()
        border.setFixedWidth(5)
        self.layout_content.addWidget(border)
        
        self.menu = AppMenu(self)
        self.layout_content.addWidget(self.menu)
        
        self.form = AppFormPC(self)
        self.layout_content.addWidget(self.form)
        
        border = QFrame()
        border.setFixedWidth(10)
        self.layout_content.addWidget(border)
        
        border = QFrame()
        border.setFixedHeight(10)
        self.layout_window.addWidget(border)
        
    def set_form(self, form: QWidget):
        self.layout_content.replaceWidget(self.form, form)
        self.form = form
 
        
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


class AppMenu(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFixedWidth(80)
        
        self.layout_menu = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_menu.setContentsMargins(0, 0, 0, 0)
        self.layout_menu.setSpacing(0)
        self.setLayout(self.layout_menu)
        self.layout_menu.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.buttons = []
        
        self.button_pc = AppMenuButton()
        self.button_pc.setIcon(Icon.PC)
        self.button_pc.setClicked(self.button_1_clicked)
        self.button_pc.setStyleSheet(f"background-color: {DefaultColor.BG_NORMAL};")
        self.buttons.append(self.button_pc)
        self.layout_menu.addWidget(self.button_pc)
        
        self.button_dex = AppMenuButton()
        self.button_dex.setIcon(Icon.DEX)
        self.button_dex.setClicked(self.button_2_clicked)
        self.buttons.append(self.button_dex)
        self.layout_menu.addWidget(self.button_dex)
        
        self.button_types = AppMenuButton()
        self.button_types.setIcon(Icon.TYPES)
        self.button_types.setClicked(self.button_3_clicked)
        self.buttons.append(self.button_types)
        self.layout_menu.addWidget(self.button_types)
        
    def button_1_clicked(self):
        self.button_pc.setStyleSheet(f"background-color: {DefaultColor.BG_NORMAL};")
        for button in self.buttons:
            if button != self.button_pc:
                button.setStyleSheet("")
        self.parent().set_form(AppFormPC(self.parent()))
        
    def button_2_clicked(self):
        self.button_dex.setStyleSheet(f"background-color: {DefaultColor.BG_NORMAL};")
        for button in self.buttons:
            if button != self.button_dex:
                button.setStyleSheet("")
        self.parent().set_form(AppFormDex(self.parent()))
        
    def button_3_clicked(self):
        self.button_types.setStyleSheet(f"background-color: {DefaultColor.BG_NORMAL};")
        for button in self.buttons:
            if button != self.button_types:
                button.setStyleSheet("")
        self.parent().set_form(AppFormTypes(self.parent()))
       
class AppMenuButton(AppButton):
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(40, 40))
        self.setFixedSize(80, 70)
        