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
from PyQt6.QtGui import QDoubleValidator
import traceback

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
        self.catnameLineEdit = QLineEdit()
        self.selectImgCard = QSelectImageCard(self.handleClearBtn)
        self.selectImgCard.connectTo(self.open_file)
        self.submitBtn = QPushButton("add category")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.catnameLabel)
        self.dialog_layout.addWidget(self.catnameLineEdit)
        self.dialog_layout.addWidget(self.selectImgCard)
        self.dialog_layout.addStretch()
        self.dialog_layout.addWidget(self.submitBtn)

    def init_addFood(self) :
        self.category_id = None
        self.foodnameLabel = QLabel("food name : ")
        self.foodnameLineEdit = QLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodpriceLineEdit = QLineEdit()
        foodpricevalidator = QDoubleValidator(0.00,1000.00,2) #1000 lang ako gi maximum, 0 minimum for like maybe if mag set sila og free stuff cuz event
        foodpricevalidator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.foodpriceLineEdit.setValidator(foodpricevalidator)
        self.selectImgCard = QSelectImageCard(self.handleClearBtn)
        self.selectImgCard.connectTo(self.open_file)
        self.categoryidLabel = QLabel("category")
        self.categoryidLineEdit = QLineEdit()
        self.categoryidLabel.hide()
        self.categoryidLineEdit.hide()
        self.submitBtn = QPushButton("add food item")
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.dialog_layout.addWidget(self.foodnameLabel)
        self.dialog_layout.addWidget(self.foodnameLineEdit)
        self.dialog_layout.addWidget(self.foodpriceLabel)
        self.dialog_layout.addWidget(self.foodpriceLineEdit)
        self.dialog_layout.addWidget(self.selectImgCard)
        self.dialog_layout.addWidget(self.categoryidLabel)
        self.dialog_layout.addWidget(self.categoryidLineEdit)
        self.dialog_layout.addStretch()
        self.dialog_layout.addWidget(self.submitBtn)
        
    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            print(checkImgSize(file_path)) #check for filesize bfore compress
            self.tempImagePath = saveImageToLocalTemp(file_path, "temp.png")
            setPixMapOf(self.selectImgCard.getLabel(), "temp.png", "temp")            

    def handleClearBtn(self) :
        self.tempImagePath = None 
        print(self.tempImagePath)

    def handleSubmitBtn(self) :
        validated = False
        if self.panelName == "category" :
            hasImg = self.tempImagePath is not None # checks if an img is appended
            catTupleToAdd = (self.catnameLineEdit.text(), None)
            if formValidated(catTupleToAdd, self.panelName) :
                imgfileName = addCategory(catTupleToAdd, hasImg)
                if hasImg: # if it has an img, move temp to assets renamed
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("added category : ", catTupleToAdd)
                validated = True
        elif self.panelName == "food" :
            hasImg = self.tempImagePath is not None
            foodTupleToAdd = (self.foodnameLineEdit.text(), self.foodpriceLineEdit.text(), None, self.category_id)
            if formValidated(foodTupleToAdd, self.panelName) :
                imgfileName = addFoodItem(foodTupleToAdd, hasImg)
                if hasImg : 
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateFoodItem")
                pubsub.publish("updateCategory")
                print("added food item : ", foodTupleToAdd)
                validated = True
        if validated :
            self.close()
            self.selectImgCard.clearImg()
            self.tempImagePath = None

class QeditDialog(QaddDialog) :
    def __init__(self, panelName, Tuple):
        super().__init__(panelName)

        if self.panelName == "category" :
            self.category_id, self.catname, self.imgfile = Tuple                
            self.init_editCategory()
        elif self.panelName == "food" :
            self.fooditem_id, self.foodname, self.price, self.imgfile, self.is_available, self.category_id = Tuple
            self.init_editFood()
        self.submitBtn.setText(f"edit {self.panelName}")


    def init_editCategory(self) :
        self.catnameLineEdit.setText(self.catname)
        self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "category")

    def init_editFood(self) :
        self.foodnameLineEdit.setText(self.foodname)
        self.foodpriceLineEdit.setText(str(self.price))
        self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "food")
        self.categoryidLabel.show()
        self.categoryidLineEdit.show()
        self.categoryidLineEdit.setText(str(self.category_id))


    def handleSubmitBtn(self) :
        if self.panelName == "category" :
            hasImg = self.tempImagePath is not None # checks if an img is appended
            catTupleToEdit = (self.catnameLineEdit.text(), None, self.category_id)
            if formValidated(catTupleToEdit, self.panelName) :
                imgfileName = editCategory(catTupleToEdit, hasImg)
                if hasImg: # if it has an img, move temp to assets renamed, will overwrite on edit
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("edited category : ", catTupleToEdit)
        elif self.panelName == "food" :
            hasImg = self.tempImagePath is not None
            foodTupleToEdit = (self.foodnameLineEdit.text(), self.foodpriceLineEdit.text(), None, self.categoryidLineEdit.text(), self.fooditem_id)
            if formValidated(foodTupleToEdit, self.panelName) :
                imgfileName = editFoodItem(foodTupleToEdit, hasImg)
                if hasImg : 
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateFoodItem")
                print("edited food item : ", foodTupleToEdit)
        self.close()
        self.selectImgCard.clearImg()
        self.tempImagePath = None