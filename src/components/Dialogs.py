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
    QFileDialog,
    QGraphicsDropShadowEffect
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
from src.components.Buttons import QPrimaryButton, QSecondaryButton, QCloseButton
from src.database.queries import fetchOrderItemsSubtotalList, fetchOrderItemsTotal
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QFont, QColor
from src.components.ScrollArea import QScrollAreaLayout
import traceback
from PyQt6 import QtWidgets


class QDialogShadowFrame(QFrame) :
    def __init__(self, child_main_layout) :
        super().__init__()
        self.setObjectName("dshadow")
        self.setStyleSheet("#dshadow{ border-radius:10px;}")
        self.setLayout(child_main_layout)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)
        shadow.setEnabled(True)
        self.raise_()



class QStyledDialog(QDialog) :
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("Background-color: white; color: black")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

    def showEvent(self, event):
        super().showEvent(event)
        # self.center_screen()


    def center_screen(self):
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
        else:
            screen = QApplication.primaryScreen()
            screen_rect = screen.availableGeometry()
            x = (screen_rect.width() - self.width()) // 2
            y = (screen_rect.height() - self.height()) // 2

        self.move(QPoint(x, y))

class QaddDialog(QStyledDialog) :
    def __init__(self, panelName, parent):
        super().__init__(parent)
        self.panelName = panelName
        self.main_layout = QVBoxLayout(self)

        self.dialog_layout = QGridLayout()
        self.tempImagePath = None
        self.shadw = QDialogShadowFrame(self.dialog_layout)
        self.shadw.setObjectName("addshadow")
        self.shadw.setStyleSheet("#addshadow {padding:20px;border-radius:10px;}")
        self.main_layout.addWidget(self.shadw)

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
            self.selectImgCard.clearButton.show()        

    def handleClearBtn(self) :
        self.tempImagePath = None 
        self.selectImgCard.clearButton.hide()

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
    def __init__(self, panelName, Tuple, parent):
        super().__init__(panelName, parent)

        if self.panelName == "category" :
            self.category_id, self.catname, self.imgfile = Tuple                
            self.init_editCategory()
        elif self.panelName == "food" :
            self.fooditem_id, self.foodname, self.price, self.imgfile, self.is_available, self.category_id = Tuple
            self.init_editFood()
        self.submitBtn.setText(f"Save")
        self.selectImgCard.getLabel().setFixedSize(150,150)


    def init_editCategory(self) :
        self.catnameLineEdit.setText(self.catname)
        if self.imgfile is not None:
            self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "category")["path"]

    def init_editFood(self) :
        self.foodnameLineEdit.setText(self.foodname)
        self.foodpriceLineEdit.setText(str(self.price))
        if self.imgfile is not None:
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
    def __init__(self, parent):
        super().__init__(parent)
        self.mainmain_layout = QVBoxLayout(self)

        self.main_layout = QVBoxLayout()
        self.mainmain_layout.addWidget(QDialogShadowFrame(self.main_layout))
        self.setFixedHeight(400)
        # self.setFixedWidth(325)

        close_btn = QCloseButton()
        close_btn.clicked.connect(self.close)

        self.close_hbox = QHBoxLayout()
        self.close_hbox.addStretch()
        self.close_hbox.addWidget(close_btn)
        self.scrollcontainer_widget = QWidget()

        self.o_idLabel = QLabel()
        self.o_idLabel.setFont(QFont("Helvitica", 15, QFont.Weight.Bold))
        self.o_idLabel.setStyleSheet("border-top: 1px solid black; border-bottom: 1px solid black;")
        self.o_idLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.foot_frame = QFrame()
        self.foot_frame.setObjectName("footframe")
        self.foot_frame.setStyleSheet("#footframe {border-top: 1px solid black; border-bottom: 1px solid black;}")
        self.foot_hbox = QHBoxLayout(self.foot_frame)
        totlam = QLabel("Total amount")
        totlam.setFont(QFont("Helvitica", 15, QFont.Weight.Bold))
        self.foot_hbox.addWidget(totlam)


        self.foot_hbox.addStretch()
        self.totalamt_label = QLabel()
        self.totalamt_label.setFont(QFont("Helvitica", 15, QFont.Weight.Bold))
        self.foot_hbox.addWidget(self.totalamt_label)

        self.main_layout.addLayout(self.close_hbox)
        self.main_layout.addWidget(self.o_idLabel)
        self.viewOrder_layout = QScrollAreaLayout(QVBoxLayout,self.main_layout)
        self.viewOrder_layout.getLayout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.foot_frame)
        pubsub.subscribe("viewClicked_event", self.setContents)
        
    def setContents(self, orderid) :
        self.orderItemsSubtotalList = fetchOrderItemsSubtotalList(orderid) 
        self.orderItemsTotal = fetchOrderItemsTotal(orderid)
        self.updateContents()
    
    def updateContents(self) :

        self.clear_layout(self.viewOrder_layout.getLayout())
        self.o_id = self.orderItemsSubtotalList[0][0]
        self.o_idLabel.setText(f"Order #{self.o_id}")        
        for oiTuple in self.orderItemsSubtotalList :
            _, fname, oiquan, subtotal = oiTuple

            labelframe = QFrame()
            labelh = QHBoxLayout(labelframe)
            labelh.setContentsMargins(0,0,0,0)

            orderitemLabel = QLabel(f"{oiquan}x {fname}")
            orderpricelabel = QLabel(f"₱{subtotal}")
            orderitemLabel.setFont(QFont("Helvitica", 13, QFont.Weight.Normal))
            orderpricelabel.setFont(QFont("Helvitica", 13, QFont.Weight.Normal))

            labelh.addWidget(orderitemLabel)
            labelh.addStretch()
            labelh.addWidget(orderpricelabel)
            self.viewOrder_layout.getLayout().addWidget(labelframe, alignment=Qt.AlignmentFlag.AlignTop)
        
            pass
        self.totalamt_label.setText(f"₱{self.orderItemsTotal}")
    
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
                elif item.layout() :
                    item.layout().deleteLater()


class QConfirmDialog(QStyledDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        self.result = False
        font = QFont("Helvetica", 12, QFont.Weight.Bold)
        self.main_layout = QVBoxLayout(self)
        layout = QVBoxLayout()
        self.main_layout.addWidget(QDialogShadowFrame(layout))

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.addStretch()
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(font)
        layout.addWidget(self.message_label)
        btn_row = QHBoxLayout()
        self.yes_btn = QPrimaryButton("Confirm")
        self.no_btn = QSecondaryButton("Cancel")
        self.yes_btn.setFont(font)
        self.no_btn.setFont(font)
        self.yes_btn.clicked.connect(self.accept)
        self.no_btn.clicked.connect(self.reject)
        btn_row.addStretch()
        btn_row.addWidget(self.no_btn)
        btn_row.addSpacing(10)
        btn_row.addWidget(self.yes_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addStretch()

    def exec(self):
        super().exec()
        return self.result

    def accept(self):
        self.result = True
        super().accept()

    def reject(self):
        self.result = False
        super().reject()
