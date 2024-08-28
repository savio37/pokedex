from src.tools.ui_bricks import *

class AppFormTypes(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_form = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_form.setContentsMargins(0, 0, 0, 0)
        self.layout_form.setSpacing(0)
        self.layout_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout_form)
        
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText("⮜ TYPE INTERACTIONS ⮞")
        label.setStyleSheet(f"""font-size: {DefaultFont.SIZE+8}pt; font-weight: bold;""")
        self.layout_form.addWidget(label)
        
        self.frame_filters = AppFrameFilters(self)
        self.layout_form.addWidget(self.frame_filters)
        
        self.frame_interactions = AppFrameInteractions(self)
        self.layout_form.addWidget(self.frame_interactions)
        
        
class AppFrameFilters(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_frame = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_frame.setContentsMargins(15, 15, 15, 15)
        self.layout_frame.setSpacing(10)
        self.setLayout(self.layout_frame)
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame.addItem(spacer)
        
        label = QLabel()
        label.setText("Types")
        self.txt_type_1 = QComboBox()
        self.txt_type_1.setFixedWidth(140)
        self.txt_type_1.setIconSize(QSize(114, 27))
        self.txt_type_2 = QComboBox()
        self.txt_type_2.setFixedWidth(140)
        self.txt_type_2.setIconSize(QSize(114, 27))
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_type_1)
        self.layout_frame.addWidget(self.txt_type_2)
        
        label = QLabel()
        label.setText("Position")
        self.txt_position = QComboBox()
        self.txt_position.setFixedWidth(160)
        self.txt_position.addItem("Attacking")
        self.txt_position.addItem("Defending")
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_position)
        
        self.txt_type_1.addItem("Any")
        self.txt_type_2.addItem("Any")
        types = db.get_type(list(range(1, 19)))
        for t in types:
            icon = QIcon(t['img'])
            self.txt_type_1.addItem(QIcon(t['img']), t['title'])
            self.txt_type_2.addItem(QIcon(t['img']), t['title'])
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame.addItem(spacer)
        
        self.txt_type_1.currentIndexChanged.connect(self.filter_types)
        self.txt_type_2.currentIndexChanged.connect(self.filter_types)
        self.txt_position.currentIndexChanged.connect(self.filter_types)
        
    def filter_types(self):
    
        frame_immune = self.parent().frame_interactions.frame_immune
        frame_resistant = self.parent().frame_interactions.frame_resistant
        frame_vulnerable = self.parent().frame_interactions.frame_vulnerable

        frame_immune.clear()
        frame_resistant.clear()
        frame_vulnerable.clear()

        
        selected_type_1 = self.txt_type_1.currentIndex()
        selected_type_2 = self.txt_type_2.currentIndex()
        selected_position = self.txt_position.currentText()

        added_immune = set()
        added_resistant = set()
        added_vulnerable = set()

        immune_list = []
        resistant_list = []
        vulnerable_list = []

        
        for selected_type_index in [selected_type_1, selected_type_2]:
            if selected_type_index != 0:  
                type_data = db.get_type(selected_type_index)

                
                if isinstance(type_data, list) and len(type_data) > 0:
                    type_data = type_data[0]
                
                if selected_position == 'Attacking':
                    type_data_mode = type_data['attacking']
                else:
                    type_data_mode = type_data['defending']


                if 'immune' in type_data_mode:
                    immune_list = type_data_mode['immune']
                    for immune_type in immune_list:
                        # Crie uma tupla única para rastreamento (pode usar outros identificadores)
                        unique_id = immune_type['id']
                        if unique_id not in added_immune:
                            frame_immune.addType(immune_type)
                            added_immune.add(unique_id)

                if 'resistant' in type_data_mode:
                    resistant_list = type_data_mode['resistant']
                    for resistant_type in resistant_list:
                        unique_id = resistant_type['id']
                        if unique_id not in added_resistant:
                            frame_resistant.addType(resistant_type)
                            added_resistant.add(unique_id)

                if 'vulnerable' in type_data_mode:
                    vulnerable_list = type_data_mode['vulnerable']
                    for vulnerable_type in vulnerable_list:
                        unique_id = vulnerable_type['id']
                        if unique_id not in added_vulnerable:
                            frame_vulnerable.addType(vulnerable_type)
                            added_vulnerable.add(unique_id)
                

                
        
class AppFrameInteractions(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_frame = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.layout_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_frame.setContentsMargins(15, 15, 15, 15)
        self.layout_frame.setSpacing(10)
        self.setLayout(self.layout_frame)
        
        self.frame_immune = AppFrameTypes(self)
        self.frame_immune.setLabel("Immune")
        self.layout_frame.addWidget(self.frame_immune)
        self.frame_resistant = AppFrameTypes(self)
        self.frame_resistant.setLabel("Resistant")
        self.layout_frame.addWidget(self.frame_resistant)
        self.frame_vulnerable = AppFrameTypes(self)
        self.frame_vulnerable.setLabel("Vulnerable")
        self.layout_frame.addWidget(self.frame_vulnerable)
        
        
class AppFrameTypes(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {DefaultColor.BG_DARK}; border-radius: 10px;")
        self.setFixedSize(300, 500)
        
        self.layout_frame = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_frame.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.layout_frame.setContentsMargins(15, 15, 15, 15)
        self.layout_frame.setSpacing(10)
        self.setLayout(self.layout_frame)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_frame.addWidget(self.label)
        
    def addType(self, type: dict):
        img = AppImage()
        img.setImage(type['img'])
        img.setFixedSize(152, 36)
        self.layout_frame.addWidget(img)
        
    def setLabel(self, text: str):
        self.label.setText(text)

    def clear(self):
        while self.layout_frame.count() > 1:  
            child = self.layout_frame.takeAt(1)  
            if child.widget():
                child.widget().deleteLater()