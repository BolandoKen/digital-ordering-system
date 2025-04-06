import os
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
    QFileDialog
)
from src.database.Categories import addCategory, editCategory
from src.database.FoodItems import addFoodItem, editFoodItem

class QaddDialog(QDialog) :
    def __init__(self, panelName, rerenderListFn):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QVBoxLayout(self)
        self.rerenderList = rerenderListFn

        if panelName == "category" :
            self.init_addCategory()
        elif panelName == "food" :
            self.init_addFood()
    
    def init_addCategory(self) :
        self.catnameLabel = QLabel("category name : ")
        self.catname = QLineEdit()
        self.imgfileLabel = QLabel("img file: ")
        self.imgfile = QPushButton("select img file")
        self.imgfile.clicked.connect(self.open_file)
        self.submitBtn = QPushButton("add food item")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catname)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.dialog_layout.addWidget(self.submitBtn)

    def init_addFood(self) :
        self.category_id = None
        self.foodnameLabel = QLabel("food name : ")
        self.foodname = QLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodprice = QLineEdit()
        self.imgfileLabel = QLabel("img file: ")
        self.imgfile = QPushButton("select img file")
        self.imgfile.clicked.connect(self.open_file)
        self.submitBtn = QPushButton("add food item")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodname)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodprice)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfile)
        self.dialog_layout.addWidget(self.submitBtn)
        
    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            self.imgfileLabel.setText(f"Selected: {file_path}")
        
    def handleSubmitBtn(self) :
        if self.panelName == "category" :
            # catTuple = (self.catname.text(), self.imgfileLabel.text())
            catTuple = (self.catname.text(), None)
            addCategory(catTuple)
            print("added category : ", catTuple)
        elif self.panelName == "food" :
            foodTuple = (self.foodname.text(), self.foodpriceLabel.text(), None, self.category_id)
            addFoodItem(foodTuple)
            print("added food item : ", foodTuple)
        self.rerenderList()
        self.close()


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