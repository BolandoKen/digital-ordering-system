from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QDialog,
    QLineEdit,
    QFileDialog,
    QComboBox
)
from src.database.queries import fetchCatList

class QCatComboBox(QComboBox) :
    def __init__(self):
        super().__init__()
        self.catList = fetchCatList("admin") 

        for cat in self.catList : 
            self.addItem(cat[1], cat[0])
        
    def setDefaultOption(self, cat_id) :
        for i in range(self.count()) :
            if int(self.itemData(i)) == int(cat_id) :
                self.setCurrentIndex(i)
                return 