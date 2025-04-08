from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)

from src.utils.PubSub import pubsub


class QFoodPanelHeader(QFrame) :
    def __init__(self, pageName):
        super().__init__()
        self.pageName = pageName
        self.state = "category"
        self.header_layout = QHBoxLayout(self)
        self.backBtn = QPushButton("<-")
        self.backBtn.clicked.connect(self.handleBackBtn)
        self.header = QLabel()
        pubsub.subscribe(f"{self.pageName}_catCardClicked", self.setHeaderState)
        self.header_layout.addWidget(self.backBtn)
        self.header_layout.addWidget(self.header)
        self.header_layout.addStretch()
        self.init_category()

    def init_category(self) :
        self.backBtn.hide()
        self.header.setText("Categories")

    def init_food(self) :
        self.backBtn.show()
        self.header.setText(self.catname)

    def setHeaderState(self, catTuple = None) :
        self.category_id, self.catname = catTuple
        self.state = "food"
        self.init_food()
    
    def handleBackBtn(self) :
        self.state = "category"
        pubsub.publish(f"{self.pageName}_backToCatClicked", None)
        self.init_category()

    




