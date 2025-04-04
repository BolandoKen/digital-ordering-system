import sys

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)

class QFoodPanel(QFrame) :
    def __init__(self, pageName):
        super().__init__()

        self.menuListCont = QMenuListContainer(pageName)

        self.food_layout = QVBoxLayout(self) # refactor to grid later on
        # will have stuff

        self.food_layout.addWidget(QLabel(pageName + " food panel, put headers and stuff here"))
        self.food_layout.addWidget(self.menuListCont) 
        # self.food_layout add (ordercart widget) # will have order cart side bar here


        

# transfer classes below to different files :
class QMenuListContainer(QFrame) :
    # contain the stacked lists
    def __init__(self, pageName) :
        super().__init__()
        self.listCont_layout = QVBoxLayout(self)
        self.stackedLists = QStackedWidget()
        self.foodList = QFoodList(pageName, self.stackedLists)
        update_listContent = self.foodList.update_listContent
        self.categoryList = QCategoryList(pageName,update_listContent, self.stackedLists)

        self.stackedLists.addWidget(self.categoryList)
        self.stackedLists.addWidget(self.foodList)
        
        self.listCont_layout.addWidget(QLabel("imagine a container of the menu"))
        self.listCont_layout.addWidget(self.stackedLists)


class QCategoryList(QFrame) : 
    # fetch all categories and list them all as btns
    # cat btns will just set stackedLists to foodlist, and update content of foodList
    def __init__(self, pageName, update_listContent, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.update_listContent = update_listContent # get update func from foodlist
        self.stackedLists = stackedLists # access parents stackedlists 
        self.catList_layout = QVBoxLayout(self)
        self.mockCatArr = ["Seafood", "Beverage"]
        self.catList_layout.addWidget(QLabel("imagine list of categories btn"))
        if self.pageName == "admin" :
            self.init_adminCatList()
        elif self.pageName == "customer" :
            self.init_customerCatList()

    def init_customerCatList(self) :
        for cat in self.mockCatArr :
            adminMockBtn = QCategoryCard(cat, self.pageName)
            adminMockBtn.clicked.connect(self.cardClicked) # put cardClicked in this class to avoid deeper passes
            self.catList_layout.addWidget(adminMockBtn)
        # no plus sign

    def init_adminCatList(self) :
        addCatBtn = QPushButton("+ add Category")
        addCatBtn.clicked.connect(self.addCategory)
        self.catList_layout.addWidget(addCatBtn)

        self.init_customerCatList()
        # has plus sign to add categories
    
    def addCategory(self) :
        print("will add category")

    def cardClicked(self) :
        category = self.sender().text()
        self.update_listContent(category)
        self.stackedLists.setCurrentIndex(1)


class QCategoryCard(QPushButton) : # at the mean time make it a QPushBtn for simplicity
    # card for each category, display name
    def __init__(self, text, pageName) :
        super().__init__(text)
        self.pageName = pageName
        self.catCard_layout = QVBoxLayout(self)

    def init_customerCategoryCard(self) :
        self.setText(self.text()) # do nothing
        # no edit/del btns

    def init_adminCategoryCard(self) :
        self.setText(self.text() + "  edit/del btns")
        # has edit/del btns , edit/trash icons in the card


class QFoodList(QFrame) :
    # fetch all food items under the category, and list them all as btns
    # food btns on click will add to order cart
    def __init__(self, pageName, stackedLists) :
        super().__init__()
        self.pageName = pageName
        self.stackedLists = stackedLists
        self.foodList_layout = QVBoxLayout(self)
        self.mockFoodlist = {
            "Seafood" : ["salamander", "shrimp", "tuna", "egg"],
            "Beverage" : ["coke", "water", "sprite"]
        }
        
    def update_listContent(self, category) :
        clear_layout(self.foodList_layout)
        self.headTitle = QLabel("")
        self.backBtn = QPushButton("<- back to cat list") # this should be inside foodlist
        self.backBtn.clicked.connect(self.backToCat)
        self.foodList_layout.addWidget(self.headTitle)
        self.foodList_layout.addWidget(self.backBtn)
        self.category = category
        if self.pageName == "admin" :
            self.init_adminFoodList()
        elif self.pageName == "customer" :
            self.init_customerFoodList()

        self.headTitle.setText(f"imagine list of fooditems under {self.category}")
        # updates the list content

    def init_customerFoodList(self) :
        foodlist = self.mockFoodlist[self.category]
        for item in foodlist :
            foodCard = QFoodItemCard(item, self.pageName)
            self.foodList_layout.addWidget(foodCard)
        # no plus sign, unable to add

    def init_adminFoodList(self) :
        addFoodBtn = QPushButton("+ add food item")
        addFoodBtn.clicked.connect(self.addFoodItem)
        self.foodList_layout.addWidget(addFoodBtn)

        self.init_customerFoodList()
        # plus sign to add food under category
    
    def addFoodItem(self) :
        print(f"will add food under {self.category}")

    def backToCat(self) :
        self.stackedLists.setCurrentIndex(0)

class QFoodItemCard(QPushButton) : # at the mean time make it a QPushBtn for simplicity
    # card for each food item, display name, img, price
    def __init__(self, text, pageName) : 
        super().__init__(text)
        self.pageName = pageName
        self.foodCard_layout = QVBoxLayout(self)
        self.clicked.connect(self.addToCart)
        if self.pageName == "admin" :
            self.init_adminFoodItemCard()
        elif self.pageName == "customer" :
            self.init_customerFoodItemCard()
    
    def init_customerFoodItemCard(self) :
        self.setText(self.text()) # do nothing
        # no edit/del btns

    def init_adminFoodItemCard(self) :
        self.setText(self.text() + "  edit/del btns")
        # has edit/del btns , edit/trash icons in the card
    
    def addToCart(self) :
        print(f"add to order cart {self.text()}")

def clear_layout(layout): 
    if layout is not None:
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i) 
            if item.widget(): 
                item.widget().deleteLater()
            elif item.spacerItem():  
                layout.removeItem(item) 