import os
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QPushButton,
    QLabel,
    QFrame,
    QDialog,
    QFileDialog,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QColor, QDoubleValidator
from src.database.queries import fetchOrderItemsSubtotalList, fetchOrderItemsTotal, ProfileQueries
from src.database.Profile import setup_pin
from src.database.Categories import addCategory, editCategory
from src.database.FoodItems import addFoodItem, editFoodItem
from src.components.ImageCard import QSelectImageCard
from src.components.ComboBox import QCatComboBox
from src.components.Buttons import QPrimaryButton, QSecondaryButton, QCloseButton
from src.components.ScrollArea import QScrollAreaLayout
from src.components.LineEdit import QFormLineEdit, QPinInputBox
from src.utils.Matplotlib import lineGraphCanvas
from src.utils.PubSub import pubsub
from src.utils.FormValid import formValidated
from src.utils.PixMap import checkImgSize, saveImageToLocalTemp, setPixMapOf, moveImageToAssets

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
        self.catnameLineEdit = QFormLineEdit()
        self.selectImgCard = QSelectImageCard(self.handleClearBtn)
        self.selectImgCard.connectTo(self.open_file)
        self.submitBtn = QPrimaryButton("Add", 70, 30 )
        self.submitBtn.clicked.connect(self.handleSubmitBtn)
        self.cancelBtn = QSecondaryButton("Cancel", 70, 30) 
        self.cancelBtn.clicked.connect(self.handleCancelBtn_cat)
        self.dialog_layout.addWidget(self.selectImgCard, 0,0,5,2)
        self.dialog_layout.addWidget(self.catnameLabel, 1,2,1,2)
        self.dialog_layout.addWidget(self.catnameLineEdit,2,2,1,3)
        self.dialog_layout.addWidget(self.cancelBtn, 4,3,1,1,)
        self.dialog_layout.addWidget(self.submitBtn, 4,4,1,1)


    def init_addFood(self) :
        self.category_id = None
        self.foodnameLabel = QLabel("food name : ")
        self.foodnameLineEdit = QFormLineEdit()
        self.foodpriceLabel = QLabel("food price : ")
        self.foodpriceLineEdit = QFormLineEdit()
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
        self.cancelBtn.clicked.connect(self.handleCancelBtn_food)
        self.dialog_layout.addWidget(self.selectImgCard,0,0,7,2)
        self.dialog_layout.addWidget(self.foodnameLabel,0,2,1,1)
        self.dialog_layout.addWidget(self.foodnameLineEdit,1,2,1,3)
        self.dialog_layout.addWidget(self.foodpriceLabel,2,2,1,1)
        self.dialog_layout.addWidget(self.foodpriceLineEdit,3,2,1,3)
        self.dialog_layout.addWidget(self.categoryidLabel,4,2,1,1)
        self.dialog_layout.addWidget(self.categoryidComboBox,5,2,1,3)
        self.dialog_layout.addWidget(self.cancelBtn, 6,3,1,1)
        self.dialog_layout.addWidget(self.submitBtn,6,4,1,1)
        
    def reset_category(self):
        self.catnameLineEdit.clear()
        if hasattr(self.selectImgCard, 'clearImg'):
            self.selectImgCard.clearImg()

    def handleCancelBtn_cat(self):
        self.reset_category()
        self.close()

    def reset_food(self):
        self.foodnameLineEdit.clear()
        self.foodpriceLineEdit.clear()
        if hasattr(self.selectImgCard, 'clearImg'):
            self.selectImgCard.clearImg()

    def handleCancelBtn_food(self):
        self.reset_food()
        self.close()

    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            print(checkImgSize(file_path)) #check for filesize bfore compress, no
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
            error_dict = formValidated(catTupleToAdd, self.panelName)
            if error_dict["final"]  :
                imgfileName = addCategory(catTupleToAdd, hasImg)
                if hasImg: # if it has an img, move temp to assets renamed
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("added category : ", catTupleToAdd)
                validated = True
                self.reset_category()
            else : 
                self.catnameLineEdit.setStateInvalid(error_dict["category_name"])

        elif self.panelName == "food" :
            hasImg = self.tempImagePath is not None
            foodTupleToAdd = (self.foodnameLineEdit.text(), self.foodpriceLineEdit.text(), None, self.category_id)
            error_dict = formValidated(foodTupleToAdd, self.panelName)
            if error_dict["final"]  :
                imgfileName = addFoodItem(foodTupleToAdd, hasImg)
                if hasImg : 
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateFoodItem")
                pubsub.publish("updateCategory")
                print("added food item : ", foodTupleToAdd)
                validated = True
                self.reset_food()
            else : 
                self.foodnameLineEdit.setStateInvalid(error_dict["food_name"])
                self.foodpriceLineEdit.setStateInvalid(error_dict["food_price"])
        if validated :
            self.close()
            self.selectImgCard.clearImg()
            self.tempImagePath = None

class QeditDialog(QaddDialog) :
    def __init__(self, panelName, parent, Tuple = None):
        super().__init__(panelName, parent)

        self.submitBtn.setText(f"Save")
        self.selectImgCard.getLabel().setFixedSize(200,200)


    def init_editCategory(self, Tuple) :
        self.category_id, self.catname, self.imgfile = Tuple                
        self.catnameLineEdit.setText(self.catname)
        if self.imgfile is not None:
            self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "category")["path"]
            self.selectImgCard.clearButton.show()

    def init_editFood(self, Tuple) :
        self.selectImgCard.clearButton.hide()
        self.categoryidLabel.hide()
        self.categoryidComboBox.hide()

        self.fooditem_id, self.foodname, self.price, self.imgfile, self.is_available, self.category_id = Tuple
        self.foodnameLineEdit.setText(self.foodname)
        self.foodpriceLineEdit.setText(str(self.price))
        self.selectImgCard.clearImg()
        self.selectImgCard.getLabel().setFixedSize(200,200)

        if self.imgfile is not None:
            self.tempImagePath = setPixMapOf(self.selectImgCard.getLabel(), self.imgfile, "food")["path"]
            self.selectImgCard.clearButton.show()

        self.categoryidLabel.show()
        self.categoryidComboBox.show()
        self.categoryidComboBox.setDefaultOption(str(self.category_id))

    def handleSubmitBtn(self) :
        validated = False
        if self.panelName == "category" :
            hasImg = self.tempImagePath is not None # checks if an img is appended
            catTupleToEdit = (self.catnameLineEdit.text(), None, self.category_id)
            error_dict = formValidated(catTupleToEdit, self.panelName) 
            if error_dict["final"] :
                imgfileName = editCategory(catTupleToEdit, hasImg)
                if hasImg: # if it has an img, move temp to assets renamed, will overwrite on edit
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateCategory")
                print("edited category : ", catTupleToEdit)
                validated = True
            else : 
                self.catnameLineEdit.setStateInvalid(error_dict["category_name"])

        elif self.panelName == "food" :
            hasImg = self.tempImagePath is not None
            foodTupleToEdit = (self.foodnameLineEdit.text(),
                                self.foodpriceLineEdit.text(),
                                None, 
                                self.categoryidComboBox.itemData(self.categoryidComboBox.currentIndex()),
                                self.fooditem_id)
            error_dict = formValidated(foodTupleToEdit, self.panelName)
            if error_dict["final"]  :
                imgfileName = editFoodItem(foodTupleToEdit, hasImg)
                if hasImg : 
                    moveImageToAssets(self.tempImagePath, self.panelName, imgfileName)
                pubsub.publish("updateFoodItem")
                pubsub.publish("updateCategory")
                print("edited food item : ", foodTupleToEdit)
                validated = True
            else : 
                self.foodnameLineEdit.setStateInvalid(error_dict["food_name"])
                self.foodpriceLineEdit.setStateInvalid(error_dict["food_price"])
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
    def __init__(self, title, message, parent=None, single_button=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 400)
        self.result = False
        self.single_button = single_button
        font = QFont("Helvetica", 40, QFont.Weight.Bold)
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
        buttonFont = QFont("Helvetica", 30, QFont.Weight.Bold)
        self.yes_btn = QPrimaryButton("Confirm", 270, 60)
        self.no_btn = QSecondaryButton("Cancel", 270, 60)
        self.yes_btn.setFont(buttonFont)
        self.no_btn.setFont(buttonFont)
        self.yes_btn.clicked.connect(self.accept)
        
        btn_row.addStretch()
        if self.single_button:
            self.no_btn.hide()
            self.yes_btn.setText("Return")
            self.yes_btn.setFixedWidth(200)

        self.no_btn.clicked.connect(self.reject)
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

class QPinDialog(QStyledDialog) :
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 300)
        self.main_layout = QVBoxLayout(self)
        self.contents_layout = QVBoxLayout()
        self.shadw = QDialogShadowFrame(self.contents_layout)
        self.main_layout.addWidget(self.shadw)

        closebtn = QCloseButton()
        closebtn.clicked.connect(self.close)
        self.mylabel = QLabel("Enter 4 digit pin")
        self.mylabel.setFont(QFont("Helvetica", 30, QFont.Weight.Bold))
        self.mylabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contents_layout.addWidget(closebtn, alignment=Qt.AlignmentFlag.AlignRight)
        self.contents_layout.addWidget(self.mylabel)
        self.digitpin = QPinInputBox()
        self.digitpin.onChange_connectTo(self.handlePin)
        self.contents_layout.addWidget(self.digitpin)
        self.result = False

    def exec(self):
        super().exec()
        return self.result
    
    def handlePin(self) :
        self.mylabel.setText("Enter 4 digit pin")
        if len(self.digitpin.text()) == 4 :
            self.submitPin()
    
    def submitPin(self) :
        if self.digitpin.text() == ProfileQueries.fetchPin() : 
            self.result = True
            super().accept()
            self.digitpin.clearText()
            return
        self.mylabel.setText("Incorrect Pin Entered.\n Try Again")
        self.digitpin.clearText()
            
    def reject(self):
        self.result = False
        super().reject()
        
class QSetupPinDialog(QStyledDialog) :
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.contents_layout = QVBoxLayout()
        self.shadw = QDialogShadowFrame(self.contents_layout)
        self.setStyleSheet("QLabel{font-family: Helvetica; font-weight: bold;}")
        self.main_layout.addWidget(self.shadw)
        closebtn = QCloseButton()
        closebtn.clicked.connect(self.close)
        self.digitpin = QPinInputBox()
        self.digitpin2 = QPinInputBox()
        self.contents_layout.addWidget(closebtn, alignment=Qt.AlignmentFlag.AlignRight)
        self.contents_layout.addWidget(QLabel("Setup 4 Digit Admin Pin"))
        self.contents_layout.addWidget(QLabel("Enter 4 digit pin"))
        self.contents_layout.addWidget(self.digitpin)
        self.mylabel = QLabel("Confirm 4 digit pin*")
        self.digitpin2.onChange_connectTo(lambda: self.mylabel.setText("Confirm 4 digit pin*"))
        self.contents_layout.addWidget(self.mylabel)
        self.contents_layout.addWidget(self.digitpin2)

        font = QFont("Helvetica", 12, QFont.Weight.Bold)
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

        self.contents_layout.addLayout(btn_row)

    def exec(self):
        super().exec()
        return self.result

    def accept(self):
        self.result = False
        if self.digitpin.text() == self.digitpin2.text() and self.digitpin.text().strip() != "" :
            self.result = True
            setup_pin(self.digitpin.text())
            self.digitpin.clearText()
            self.digitpin2.clearText()
            super().accept()
            return
        self.mylabel.setText("Confirm 4 digit pin* - pins do not match!")
        self.digitpin2.clearText()

    def reject(self):
        self.result = False
        super().reject()


class QChangePfpDialog(QStyledDialog) :
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.contents_layout = QVBoxLayout()
        self.shadw = QDialogShadowFrame(self.contents_layout)
        pushbtn_style = "font-family: Helvetica; font-weight: bold; font:20px; border: 1px solid #d1d1d1; padding: 10px;"
        self.main_layout.addWidget(self.shadw)

        self.contents_layout.setContentsMargins(0,0,0,0)
        self.contents_layout.setSpacing(0)
        self.mylabel = QLabel("Change Profile Photo")
        self.mylabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mylabel.setFixedHeight(75)
        self.mylabel.setStyleSheet("background-color: #FFCA40; font-family: Helvetica; font-weight: 1000;font: 25px; border: 1px solid #d1d1d1; padding: 20px;" + "border-top-left-radius: 10px; border-top-right-radius:10px;")
        self.changePhotoBtn = QPushButton("Change Photo")
        self.changePhotoBtn.setStyleSheet(pushbtn_style + "color: #72CEFF")
        self.changePhotoBtn.clicked.connect(self.open_file)
        self.removeCurrentBtn = QPushButton("Remove Current Photo")
        self.removeCurrentBtn.setStyleSheet(pushbtn_style + "color: #C8161D")
        self.removeCurrentBtn.clicked.connect(self.handleClearBtn)
        self.cancelBtn = QPushButton("cancel")
        self.cancelBtn.setStyleSheet(pushbtn_style + "border-bottom-left-radius: 10px; border-bottom-right-radius:10px;")
        self.cancelBtn.clicked.connect(self.close)
        self.changePhotoBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.removeCurrentBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancelBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.contents_layout.addWidget(self.mylabel)
        self.contents_layout.addWidget(self.changePhotoBtn)
        self.contents_layout.addWidget(self.removeCurrentBtn)
        self.contents_layout.addWidget(self.cancelBtn)

        self.tempImagePath = None
        pubsub.subscribe("updateProfile", self.setTempImgPath)

    
    def set_profileIcon(self, profileIcon) :
        self.profileIcon = profileIcon
        self.setTempImgPath()
    
    def setTempImgPath(self, e= None) :
        self.tempImagePath = self.profileIcon.init_profileImg()

    def resetProfileIcon(self) :
        self.tempImagePath = self.profileIcon.init_profileImg()


    def open_file(self):
        home_dir = os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            print(checkImgSize(file_path)) #check for filesize bfore compress, no
            self.tempImagePath = saveImageToLocalTemp(file_path, "temp.png")
            setPixMapOf(self.profileIcon, "temp.png", "temp")  
        self.close()
    
    def handleClearBtn(self) :
        self.tempImagePath = None
        self.profileIcon.clearImg()
        self.profileIcon.setScaledContents(True)
        self.profileIcon.setFixedSize(150,150)
        self.close()



class QFoodItemStatsDialog(QStyledDialog) :
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.contents_layout = QVBoxLayout()
        self.shadw = QDialogShadowFrame(self.contents_layout)
        self.main_layout.addWidget(self.shadw)

        closebtn = QCloseButton()
        closebtn.clicked.connect(self.close)
        self.setStyleSheet("QLabel{font-family: Helvetica; font: 15px;}")

        self.imglabel = QLabel()
        self.foodnamelabel = QLabel()
        self.foodnamelabel.setStyleSheet("font-family: Helvetica; font: 30px; font-weight: bold;")
        self.categorynamelabel = QLabel()
        self.categorynamelabel.setFixedWidth(130)
        self.categorynamelabel.setStyleSheet("font-family: Helvetica; font: 15px; font-weight: bold;border-bottom: 1px solid black; ")

        self.countLabel = QLabel()
        self.peakLabel = QLabel()
        self.datetitleLabel = QLabel()

        self.contents_layout.setContentsMargins(50, 10,10,10)
        
        self.canvas = lineGraphCanvas()

        details_vbox = QVBoxLayout()
        details_vbox.addSpacing(60)
        details_vbox.addWidget(self.imglabel, alignment=Qt.AlignmentFlag.AlignLeft)
        details_vbox.addWidget(self.foodnamelabel, alignment=Qt.AlignmentFlag.AlignLeft)
        details_vbox.addWidget(self.categorynamelabel, alignment=Qt.AlignmentFlag.AlignLeft)
        details_vbox.addWidget(self.datetitleLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        details_vbox.addWidget(self.countLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        details_vbox.addWidget(self.peakLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        details_vbox.addStretch()

        contentshbox = QHBoxLayout()
        contentshbox.addLayout(details_vbox)
        contentshbox.addWidget(self.canvas)

        self.contents_layout.addWidget(closebtn, alignment=Qt.AlignmentFlag.AlignRight)
        self.contents_layout.addLayout(contentshbox)
    
    def setContents(self, fooditem_id, foodname, cat, imgfile, times, DateRange = None) :
        setPixMapOf(self.imglabel, imgfile, "food")
        self.foodnamelabel.setText(foodname)
        self.categorynamelabel.setText(cat)
        self.countLabel.setText(f"Times Ordered: {times}")
        self.canvas.setContents(fooditem_id, DateRange)
        self.peakLabel.setText(self.canvas.peak)
        self.datetitleLabel.setText(self.canvas.mytitle)
