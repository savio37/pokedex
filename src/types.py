from src.tools.ui_bricks import *

class AppFormTypes(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_form = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_form.setContentsMargins(0, 0, 0, 0)
        self.layout_form.setSpacing(0)
        self.layout_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout_form)
        
        self.logo = AppImage()
        self.logo.setIcon(Icon.TYPES)
        self.logo.setFixedSize(128, 128)
        self.layout_form.addWidget(self.logo)