import sys
from PyQt6.QtWidgets import QApplication
from src.root import AppWindowRoot    
          
app = QApplication(sys.argv)
root = AppWindowRoot()
root.showFullScreen()
sys.exit(app.exec())