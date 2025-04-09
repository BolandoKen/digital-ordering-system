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
from src.utils.PubSub import pubsub
from src.utils.FormValid import formValidated
from src.database.Categories import addCategory, editCategory
from src.database.FoodItems import addFoodItem, editFoodItem
from src.utils.PixMap import checkImgSize, saveImageToLocalTemp, setPixMapOf, moveImageToAssets
from src.components.Buttons import QImageButton
from src.components.ImageCard import QSelectImageCard
from PyQt6.QtGui import QPixmap


class QaddDialog(QDialog) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QVBoxLayout(self)
        self.tempImagePath = None

        if panelName == "category" :
            self.init_addCategory()
        elif panelName == "food" :
            self.init_addFood()
    
    def init_addCategory(self) :
        self.catnameLabel = QLabel("category name : ")
        self.catname = QLineEdit()
        self.selectImgCard = QSelectImageCard()
        self.selectImgCard.connectTo(self.open_file)
        self.submitBtn = QPushButton("add category")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catname)
        self.dialog_layout.addWidget(self.selectImgCard)
        self.dialog_layout.addStretch()
        self.dialog_layout.addWidget(self.submitBtn)

    def init_addFood(self) :
        self.category_id = None
        self.foodnameLabel = QLabel("food name : ")
        self.foodname = QLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodprice = QLineEdit()
        self.selectImgCard = QSelectImageCard()
        self.selectImgCard.connectTo(self.open_file)
        self.submitBtn = QPushButton("add food item")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodname)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodprice)
        self.dialog_layout.addWidget(self.selectImgCard)
        self.dialog_layout.addStretch()
        self.dialog_layout.addWidget(self.submitBtn)
        
    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            print(checkImgSize(file_path)) #check for filesize bfore compress
            self.tempImagePath = saveImageToLocalTemp(file_path, "temp.png")
            setPixMapOf(self.selectImgCard.getLabel(), "temp.png", "temp")            
        
    def handleSubmitBtn(self) :
        if self.panelName == "category" :
            hasImg = self.tempImagePath is not None # checks if an img is appended
            catTuple = (self.catname.text(), None)
            if formValidated(catTuple, self.panelName) :
                imgfileName = addCategory(catTuple, hasImg)
                if hasImg:
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("added category : ", catTuple)
        elif self.panelName == "food" :
            foodTuple = (self.foodname.text(), self.foodprice.text(), None, self.category_id)
            if formValidated(foodTuple, self.panelName) :
                addFoodItem(foodTuple)
                pubsub.publish("updateFoodItem")
                print("added food item : ", foodTuple)
        self.close()
        self.selectImgCard.clearImg()
        self.tempImagePath = None

class QeditDialog(QDialog) :
    def __init__(self, panelName, Tuple):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QVBoxLayout(self)

        if panelName == "category" :
            self.category_id, self.catname, self.imgfile = Tuple
            self.init_editCategory()
        elif panelName == "food" :
            self.fooditem_id, self.foodname, self.price, self.imgfile, self.category_id = Tuple
            self.init_editFood()
    
    def init_editCategory(self) :
        self.catnameLabel = QLabel("category name : ")
        self.catnameLineEdit = QLineEdit()
        self.catnameLineEdit.setText(self.catname)
        self.imgfileLabel = QLabel("img file: ")
        self.imgfileBtn = QPushButton("select img file")
        self.imgfileBtn.clicked.connect(self.open_file)
        self.submitBtn = QPushButton("edit category")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catnameLineEdit)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfileBtn)
        self.dialog_layout.addWidget(self.submitBtn)

    def init_editFood(self) :
        self.foodnameLabel = QLabel("food name : ")
        self.foodnameLineEdit = QLineEdit()
        self.foodnameLineEdit.setText(self.foodname)
        self.foodpriceLabel = QLabel("food price : ")
        self.foodpriceLineEdit = QLineEdit()
        self.foodpriceLineEdit.setText(str(self.price))
        self.imgfileLabel = QLabel("img file: ")
        self.imgfileBtn = QPushButton("select img file")
        self.imgfileBtn.clicked.connect(self.open_file)
        self.categoryidLabel = QLabel("category") 
        self.categoryidLineEdit = QLineEdit()
        self.categoryidLineEdit.setText(str(self.category_id))
        self.submitBtn = QPushButton("edit food item")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodnameLineEdit)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodpriceLineEdit)
        self.dialog_layout.addWidget(self.imgfileLabel)
        self.dialog_layout.addWidget(self.imgfileBtn)
        self.dialog_layout.addWidget(self.categoryidLabel)
        self.dialog_layout.addWidget(self.categoryidLineEdit)
        self.dialog_layout.addWidget(self.submitBtn)
        
    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            self.imgfileLabel.setText(f"Selected: {file_path}")
        
    def handleSubmitBtn(self) :
        if self.panelName == "category" :
            catTuple = (self.catnameLineEdit.text(), None, self.category_id)
            if formValidated(catTuple, self.panelName) :
                editCategory(catTuple)
                pubsub.publish("updateCategory")
                print("edit category : ", catTuple)
        elif self.panelName == "food" :
            foodTuple = (self.foodnameLineEdit.text(), self.foodpriceLineEdit.text(), None, self.categoryidLineEdit.text(), self.fooditem_id)
            if formValidated(catTuple, self.panelName) :
                editFoodItem(foodTuple)
                pubsub.publish("updateFoodItem")
                print("edit food item : ", foodTuple)
        self.close()
