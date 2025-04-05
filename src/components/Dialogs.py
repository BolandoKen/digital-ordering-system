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
    QLineEdit
)

class QaddDialog(QDialog) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QVBoxLayout(self)

        if panelName == "category" :
            self.init_addCategory()
        elif panelName == "food" :
            self.init_addFood()
    
    def init_addCategory(self) :
        self.catnameLabel = QLabel("category name : ")
        self.catname = QLineEdit()
        self.imgfileLabel = QLabel("img file : ")
        self.imgfile = QLineEdit()
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catname)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.submitBtn = QPushButton("add category")
        self.dialog_layout.addWidget(self.submitBtn)


    def init_addFood(self) :
        self.foodnameLabel = QLabel("food name : ")
        self.foodname = QLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodprice = QLineEdit()
        self.imgfileLabel = QLabel("img file : ")
        self.imgfile = QLineEdit()
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodname)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodprice)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.submitBtn = QPushButton("add food item")
        self.dialog_layout.addWidget(self.submitBtn)


class QeditDialog(QDialog) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QVBoxLayout(self)

        if panelName == "category" :
            self.init_addCategory()
        elif panelName == "food" :
            self.init_addFood()
    
    def init_addCategory(self) :
        self.catnameLabel = QLabel("category name : ")
        self.catname = QLineEdit()
        self.imgfileLabel = QLabel("img file : ")
        self.imgfile = QLineEdit()
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catname)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.submitBtn = QPushButton("add category")
        self.dialog_layout.addWidget(self.submitBtn)


    def init_addFood(self) :
        self.foodnameLabel = QLabel("food name : ")
        self.foodname = QLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodprice = QLineEdit()
        self.imgfileLabel = QLabel("img file : ")
        self.imgfile = QLineEdit()
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodname)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodprice)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.submitBtn = QPushButton("add food item")
        self.dialog_layout.addWidget(self.submitBtn)