from PyQt6.QtGui import QMouseEvent
from src.tools.ui_bricks import *
from src.dex_entry import *

class AppFormDex(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_form = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout_form.setContentsMargins(0, 0, 0, 0)
        self.layout_form.setSpacing(0)
        self.setLayout(self.layout_form)
        self.layout_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_form.setContentsMargins(15, 15, 15, 15)
        self.layout_form.setSpacing(15)
        
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText("⮜ POKÉDEX ⮞")
        label.setStyleSheet(f"""font-size: {DefaultFont.SIZE+8}pt; font-weight: bold;""")
        self.layout_form.addWidget(label)
        
        self.frame_species = AppFrameCards(self)
        self.frame_filters = AppFrameFilters(self)
        self.layout_form.addWidget(self.frame_filters)
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.frame_species)
        self.layout_form.addWidget(self.scroll_area)
        
        self.frame_filters.filter_species()
        
        
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
        label.setText("Number")
        self.txt_num = QLineEdit()
        self.txt_num.setFixedWidth(80)
        self.txt_num.setValidator(QIntValidator(0, 999))
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_num)
        
        label = QLabel()
        label.setText("Name")
        self.txt_name = QLineEdit()
        self.txt_name.setFixedWidth(200)
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_name)
        
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
        
        self.check_evo = QCheckBox()
        self.check_evo.setText("Show Family")
        self.check_evo.setChecked(False)
        self.check_evo.hide()
        self.layout_frame.addWidget(self.check_evo)
        
        self.txt_type_1.addItem("Any")
        self.txt_type_2.addItem("Any")
        types = db.get_type(list(range(1, 19)))
        for t in types:
            self.txt_type_1.addItem(QIcon(t['img']), t['title'])
            self.txt_type_2.addItem(QIcon(t['img']), t['title'])
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame.addItem(spacer)
        
        self.txt_num.textChanged.connect(lambda: self.filter_species())
        self.txt_name.textChanged.connect(lambda: self.filter_species())
        self.txt_type_1.currentTextChanged.connect(lambda: self.filter_species())
        self.txt_type_2.currentTextChanged.connect(lambda: self.filter_species())
        self.check_evo.stateChanged.connect(lambda: self.filter_species())
        
    def filter_species(self):
        id = self.txt_num.text()
        id = None if id == '' else int(id)
        name = self.txt_name.text()
        type_1 = self.txt_type_1.currentText()
        type_2 = self.txt_type_2.currentText()
        family = self.check_evo.isChecked()
        
        if id != None or name != '' or type_1 != 'Any' or type_2 != 'Any':
            self.check_evo.show()
        else:
            self.check_evo.setChecked(False)
            self.check_evo.hide()
        
        species = db.get_species(id, name, type_1, type_2, family)
        
        frame_species:AppFrameCards = self.parent().frame_species
        frame_species.load_species(species)

        
class AppFrameCards(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_frame = QGridLayout()
        self.layout_frame.setContentsMargins(0, 0, 0, 0)
        self.layout_frame.setSpacing(0)
        self.layout_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_frame.setSpacing(20)
        self.setLayout(self.layout_frame)
    
    def load_species(self, species):
        while self.layout_frame.count():
            child = self.layout_frame.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for i, specie in enumerate(species):
            card = AppCardSpecies(self)
            card.set_species(specie)
            self.layout_frame.addWidget(card, i // 5, i % 5, 1, 1)

        
class AppCardSpecies(AppCard):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.pokemon = None
        self.popup = AppWindowEntry()
        
        self.label_num = QLabel()
        self.layout_frame.addWidget(self.label_num, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.label_especie = QLabel()
        self.layout_frame.addWidget(self.label_especie, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        self.img_especie = AppImage()
        self.img_especie.setFixedSize(160, 160)
        self.layout_frame.addWidget(self.img_especie, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        
        self.img_tipo_1 = AppImage()
        self.img_tipo_1.setFixedSize(114, 27)
        
        self.img_tipo_2 = AppImage()
        self.img_tipo_2.setFixedSize(114, 27)
        
    def mousePressEvent(self, a0: QMouseEvent | None):
        super().mousePressEvent(a0)
        self.popup.show()
        
    def set_species(self, species: dict):
        self.pokemon = species
        self.label_num.setText(f"#{species['id']:03}")
        self.label_especie.setText(species['name'])
        self.img_especie.setImage(species['img'])
        
        self.img_tipo_1.setImage(species['types'][0]['img'])
        if len(species['types']) > 1:
            self.img_tipo_2.setImage(species['types'][1]['img'])
            self.layout_frame.addWidget(self.img_tipo_1, 2, 0, 1, 1, Qt.AlignmentFlag.AlignBottom)
            self.layout_frame.addWidget(self.img_tipo_2, 2, 1, 1, 1, Qt.AlignmentFlag.AlignBottom)
        else:
            self.layout_frame.addWidget(self.img_tipo_1, 2, 0, 1, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        
        self.popup.form.set_species(species)
        self.update()
        self.parent().update()
        