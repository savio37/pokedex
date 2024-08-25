from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from src.tools.globals import *


class AppButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.setFixedWidth(120)
        self.setIconSize(QSize(22, 22))
        
        self.anim_group = QParallelAnimationGroup()
        
        self.color_effect = QGraphicsColorizeEffect()
        self.color_effect.setColor(QColor(55, 55, 80))
        self.color_effect.setStrength(0.0)
        self.setGraphicsEffect(self.color_effect)
        
        self.anim_color = QPropertyAnimation(self.color_effect, b"strength")
        self.anim_color.setDuration(200)
        self.anim_color.setEasingCurve(QEasingCurve.Type.InCubic)
        
        self.anim_group.addAnimation(self.anim_color)
        
    def enterEvent(self, event):
        self.anim_group.setDirection(QPropertyAnimation.Direction.Forward)
        if self.anim_group.state() == QPropertyAnimation.State.Stopped:
            self.anim_color.setStartValue(0.0)
            self.anim_color.setEndValue(0.6)
            
            self.anim_group.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.anim_group.setDirection(QPropertyAnimation.Direction.Backward)
        if self.anim_group.state() == QPropertyAnimation.State.Stopped:
            self.anim_group.start()
        super().leaveEvent(event)
    
    def setClicked(self, func: callable):
        self.clicked.connect(func)
        
    def setIcon(self, icon: str):
        super().setIcon(QIcon(icon))

        
class AppTitlebarButton(AppButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(45, 30)
        self.setIconSize(QSize(20, 20))


class AppCard(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(f"""background-color: {DefaultColor.BG_LIGHT}; border-radius: 20px;""")
        self.setFixedSize(250, 250)
        self.layout_frame = QGridLayout()
        self.layout_frame.setContentsMargins(15, 15, 15, 15)
        self.layout_frame.setSpacing(0)
        self.setLayout(self.layout_frame)
        
    def enterEvent(self, a0: QEvent | None):
        super().enterEvent(a0)
        self.setStyleSheet(f"""background-color: {DefaultColor.BG_DARK}; border-radius: 20px;""")
        
    def leaveEvent(self, a0: QEvent | None):
        super().leaveEvent(a0)
        self.setStyleSheet(f"""background-color: {DefaultColor.BG_LIGHT}; border-radius: 20px;""")
        

class AppImage(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(True)
        
    def setImage(self, path: str):
        self.setPixmap(QPixmap(path))
        
    def setIcon(self, icon: str):
        self.setImage(icon)
        