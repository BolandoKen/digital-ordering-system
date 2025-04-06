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
        # self.label = QLabel("No file selected")
        # self.button = QPushButton("Open File")
        # self.button.clicked.connect(self.open_file)
        # self.dialog_layout.addWidget(self.label)
        # self.dialog_layout.addWidget(self.button)


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_path:
            self.label.setText(f"Selected: {file_path}")

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