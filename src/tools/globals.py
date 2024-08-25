from src.tools.database import *

db = FacadeDB()
    

class Icon:
    __path = "assets/icons/"
    
    #control
    ARROW_DOWN = __path + "control/arrow_down.png"
    ARROW_UP = __path + "control/arrow_up.png"
    CHECKED = __path + "control/checked.png"
    DELETE = __path + "control/delete.png"
    SAVE = __path + "control/save.png"
    EDIT = __path + "control/edit.png"
    SELECT = __path + "control/select.png"
    
    #menu
    PC = __path + "menu/pc.png"
    DEX = __path + "menu/dex.png"
    TYPES = __path + "menu/types.png"
    
    #titlebar
    CLOSE = __path + "titlebar/close.png"
    MAXIMIZE = __path + "titlebar/maximize.png"
    MINIMIZE = __path + "titlebar/minimize.png"
    RESTORE = __path + "titlebar/restore.png"
    
    
class DefaultFont:
    FAMILY = "lexend"
    SIZE = 14
    

class DefaultColor:
    BG_LIGHT = "#445"
    BG_NORMAL = "#334"
    BG_DARK = "#223"
    TEXT = "#eee"
        

class DefaultStyle:
    APP_WINDOW = f"""
        *{{
            font-weight: normal;
            font-family: {DefaultFont.FAMILY};
            font-size: {DefaultFont.SIZE}pt;
            border: none;
            background-color: {DefaultColor.BG_NORMAL};
            color: {DefaultColor.TEXT};
        }}
        
        QFrame, AppButton{{
            font-weight: bold;
            background-color: {DefaultColor.BG_DARK};
            color: {DefaultColor.TEXT};
            text-align: center;
        }}
        
        AppMenuButton{{
            border-top-left-radius: 5px; 
            border-bottom-left-radius: 5px;
        }}
        
        AppFormDex, AppFormDex QFrame, AppFormPC, AppFormPC QFrame, AppFormTypes, AppFormTypes QFrame {{
            background-color: {DefaultColor.BG_NORMAL};
            color: {DefaultColor.TEXT};
        }}
        
        QComboBox, QLineEdit, QTableView, QCheckBox::indicator {{
            background-color: {DefaultColor.BG_LIGHT};
            border-radius: 5px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
        }}
        
        QComboBox:on {{
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        
        QComboBox::drop-down, QComboBox::down-arrow, QComboBox::down-arrow:on {{
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            background-color: {DefaultColor.BG_DARK};
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: url({Icon.ARROW_DOWN});
        }}
        
        QComboBox::down-arrow:on {{
            image: url({Icon.ARROW_UP});
        }}
        
        QComboBox QAbstractItemView, QProgressBar, QCheckBox::indicator:unchecked {{
            background-color: {DefaultColor.BG_LIGHT};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {DefaultColor.BG_DARK};
        }}
        
        AppImage, QLabel {{
            background-color: transparent;
        }}
        
        """