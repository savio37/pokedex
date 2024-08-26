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
        border.setFixedWidth(10)
        self.layout_content.addWidget(border)
        
        self.form = AppFormEntry(self)
        self.layout_content.addWidget(self.form)
        
        border = QFrame()
        border.setFixedWidth(10)
        self.layout_content.addWidget(border)
        
        border = QFrame()
        border.setFixedHeight(10)
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
        
    def set_species(self, species: dict):
        pass