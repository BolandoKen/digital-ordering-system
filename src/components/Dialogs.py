import os
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
from src.components.ComboBox import QCatComboBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QDoubleValidator
from src.components.Buttons import QPrimaryButton, QSecondaryButton
from src.database.queries import fetchOrderItemsSubtotalList, fetchOrderItemsTotal
import traceback


class QStyledDialog(QDialog) :
    def __init__(self):
        super().__init__()
        self.setStyleSheet("Background-color: white; color: black")


class QaddDialog(QStyledDialog) :
    def __init__(self, panelName):
        super().__init__()
        self.panelName = panelName
        self.dialog_layout = QGridLayout(self)
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
        self.submitBtn = QPrimaryButton("Add", 70, 30 )
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.cancelBtn = QSecondaryButton("Cancel", 70, 30) 
        self.cancelBtn.clicked.connect(self.close)
        self.dialog_layout.addWidget(self.selectImgCard, 0,0,5,2)
        self.dialog_layout.addWidget(self.catnameLabel, 1,2,1,2)
        self.dialog_layout.addWidget(self.catnameLineEdit,2,2,1,3)
        self.dialog_layout.addWidget(self.cancelBtn, 4,3,1,1,)
        self.dialog_layout.addWidget(self.submitBtn, 4,4,1,1)

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
        self.categoryidLabel.hide()
        self.categoryidComboBox = QCatComboBox()
        self.categoryidComboBox.hide()
        self.submitBtn = QPrimaryButton("Add", 70, 30 )
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.cancelBtn = QSecondaryButton("Cancel", 70, 30) 
        self.cancelBtn.clicked.connect(self.close)
        self.dialog_layout.addWidget(self.selectImgCard,0,0,7,2)
        self.dialog_layout.addWidget(self.foodnameLabel,0,2,1,1)
        self.dialog_layout.addWidget(self.foodnameLineEdit,1,2,1,3)
        self.dialog_layout.addWidget(self.foodpriceLabel,2,2,1,1)
        self.dialog_layout.addWidget(self.foodpriceLineEdit,3,2,1,3)
        self.dialog_layout.addWidget(self.categoryidLabel,4,2,1,1)
        self.dialog_layout.addWidget(self.categoryidComboBox,5,2,1,3)
        self.dialog_layout.addWidget(self.cancelBtn, 6,3,1,1)
        self.dialog_layout.addWidget(self.submitBtn,6,4,1,1)
        
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
        self.submitBtn.setText(f"Save")


    def init_editCategory(self) :
        self.catnameLineEdit.setText(self.catname)
        self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "category")["path"]

    def init_editFood(self) :
        self.foodnameLineEdit.setText(self.foodname)
        self.foodpriceLineEdit.setText(str(self.price))
        self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "food")["path"]
        self.categoryidLabel.show()
        self.categoryidComboBox.show()
        self.categoryidComboBox.setDefaultOption(str(self.category_id))

    def handleSubmitBtn(self) :
        validated = False
        if self.panelName == "category" :
            hasImg = self.tempImagePath is not None # checks if an img is appended
            catTupleToEdit = (self.catnameLineEdit.text(), None, self.category_id)
            if formValidated(catTupleToEdit, self.panelName) :
                imgfileName = editCategory(catTupleToEdit, hasImg)
                if hasImg: # if it has an img, move temp to assets renamed, will overwrite on edit
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("edited category : ", catTupleToEdit)
                validated = True
        elif self.panelName == "food" :
            hasImg = self.tempImagePath is not None
            foodTupleToEdit = (self.foodnameLineEdit.text(),
                                self.foodpriceLineEdit.text(),
                                None, 
                                self.categoryidComboBox.itemData(self.categoryidComboBox.currentIndex()),
                                self.fooditem_id)
            if formValidated(foodTupleToEdit, self.panelName) :
                imgfileName = editFoodItem(foodTupleToEdit, hasImg)
                if hasImg : 
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateFoodItem")
                pubsub.publish("updateCategory")
                print("edited food item : ", foodTupleToEdit)
                validated = True
        if validated :
            self.close()
            self.selectImgCard.clearImg()
            self.tempImagePath = None


class QviewOrderDialog(QStyledDialog) :
    def __init__(self):
        super().__init__()
        self.viewOrder_layout = QVBoxLayout(self)
        pubsub.subscribe("viewClicked_event", self.setContents)
        self.oldid = None
        
    def setContents(self, orderid) :
        self.orderItemsSubtotalList = fetchOrderItemsSubtotalList(orderid) 
        self.orderItemsTotal = fetchOrderItemsTotal(orderid)
        if self.oldid != orderid :
            self.updateContents()
        self.oldid = orderid
    
    def updateContents(self) :
        self.clear_layout(self.viewOrder_layout)
        self.o_id = self.orderItemsSubtotalList[0][0]
        o_idLabel = QLabel(f"Order #{self.o_id}")
        self.viewOrder_layout.addWidget(o_idLabel)        
        for oiTuple in self.orderItemsSubtotalList :
            _, fname, oiquan, subtotal = oiTuple
            orderitemLabel = QLabel(f"{oiquan}x {fname} ₱{subtotal}")
            self.viewOrder_layout.addWidget(orderitemLabel)
        
            pass
        self.viewOrder_layout.addWidget(QLabel(f"Total Amount: ₱{self.orderItemsTotal}"))
    
    def clear_layout(self, layout): 
        print('rerendered viewOrder Dialog')
        if layout is not None:
            for i in reversed(range(layout.count())): 
                item = layout.takeAt(i) 
                if item.widget(): 
                    item.widget().hide() # for some reason u can see previous in the bg
                    item.widget().deleteLater()
                elif item.spacerItem():  
                    layout.removeItem(item)   


        