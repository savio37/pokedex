from PyQt6.QtGui import QMouseEvent
from src.tools.ui_bricks import *
from src.pc_entry import *

class AppFormPC(QFrame):
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
        label.setText("⮜ PC ⮞")
        label.setStyleSheet(f"""font-size: {DefaultFont.SIZE+8}pt; font-weight: bold;""")
        self.layout_form.addWidget(label)
        
        self.frame_cards = AppFrameCards(self)
        self.frame_filters = AppFrameFilters(self)
        self.layout_form.addWidget(self.frame_filters)
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.frame_cards)
        self.layout_form.addWidget(self.scroll_area)
        
        self.frame_filters.filter_pokemon()
        
        
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
        label.setText("Species")
        self.txt_name = QLineEdit()
        self.txt_name.setFixedWidth(200)
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_name)
        
        label = QLabel()
        label.setText("Nickname")
        self.txt_nickname = QLineEdit()
        self.txt_nickname.setFixedWidth(200)
        self.layout_frame.addWidget(label)
        self.layout_frame.addWidget(self.txt_nickname)
        
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
        
        self.txt_type_1.addItem("Any")
        self.txt_type_2.addItem("Any")
        types = db.get_type(list(range(1, 19)))
        for t in types:
            self.txt_type_1.addItem(QIcon(t['img']), t['title'])
            self.txt_type_2.addItem(QIcon(t['img']), t['title'])
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame.addItem(spacer)
        
        self.txt_name.textChanged.connect(lambda: self.filter_pokemon())
        self.txt_nickname.textChanged.connect(lambda: self.filter_pokemon())
        self.txt_type_1.currentTextChanged.connect(lambda: self.filter_pokemon())
        self.txt_type_2.currentTextChanged.connect(lambda: self.filter_pokemon())
        
    def filter_pokemon(self):
        name = self.txt_name.text()
        nickname = self.txt_nickname.text()
        type_1 = self.txt_type_1.currentText()
        type_2 = self.txt_type_2.currentText()
        
        pokemons = db.get_pokemon(name, nickname, type_1, type_2)
        
        frame_cards:AppFrameCards = self.parent().frame_cards
        frame_cards.load_pokemons(pokemons)

        
class AppFrameCards(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.layout_frame = QGridLayout()
        self.layout_frame.setContentsMargins(0, 0, 0, 0)
        self.layout_frame.setSpacing(0)
        self.layout_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_frame.setSpacing(20)
        self.setLayout(self.layout_frame)
    
    def load_pokemons(self, pokemons):
        while self.layout_frame.count():
            child = self.layout_frame.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for i, pokemon in enumerate(pokemons):
            card = AppCardPokemon(self)
            card.set_pokemon(pokemon)
            self.layout_frame.addWidget(card, i // 5, i % 5, 1, 1)

        
class AppCardPokemon(AppCard):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.pokemon = None
        self.popup = AppWindowEntry()
        
        self.label_especie = QLabel()
        self.layout_frame.addWidget(self.label_especie, 0, 0, 1, 2, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
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
        
    def set_pokemon(self, pokemon: dict):
        self.pokemon = pokemon
        self.label_especie.setText(pokemon['name'])
        if 'nickname' in pokemon:
            self.label_especie.setText(f"{pokemon['nickname']} ({pokemon['name']})")
        self.img_especie.setImage(pokemon['img'])
        
        self.img_tipo_1.setImage(pokemon['types'][0]['img'])
        if len(pokemon['types']) > 1:
            self.img_tipo_2.setImage(pokemon['types'][1]['img'])
            self.layout_frame.addWidget(self.img_tipo_1, 2, 0, 1, 1, Qt.AlignmentFlag.AlignBottom)
            self.layout_frame.addWidget(self.img_tipo_2, 2, 1, 1, 1, Qt.AlignmentFlag.AlignBottom)
        else:
            self.layout_frame.addWidget(self.img_tipo_1, 2, 0, 1, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        
        self.popup.form.set_pokemon(pokemon)
        self.update()
        self.parent().update()
        