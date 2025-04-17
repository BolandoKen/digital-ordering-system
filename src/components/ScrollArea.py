
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
    QScrollArea
)
from PyQt6.QtCore import Qt

class QScrollAreaLayout(QScrollArea) :
    def __init__(self, QLayoutType, parentWidget, component = "list"):
        super().__init__()
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.setWidget(self.container)
        if component == "list" : 
            mywidth = "10px"
        elif component == "sidebar" :
            mywidth = "5px"
        #styles derived from https://forum.qt.io/topic/41040/pyqt-custom-scrollbar-design-solved/5
        self.setStyleSheet(f"""QScrollBar:vertical {{
                            width: {mywidth};
                            margin: 0;
                           border: none;

                        }}
                        QScrollBar::handle:vertical {{
                            min-height: 10px;
                            border: none;
                           background-color: #D9D9D9;
                           border-radius: 5px;
                        }}
                        QScrollArea {{
                           padding: 0px;
                           border:none;
                           }}
                        QScrollBar::add-line:vertical,
                        QScrollBar::sub-line:vertical,
                        QScrollBar::up-arrow:vertical,
                        QScrollBar::down-arrow:vertical{{
                           background: none;
                            height: 0px; 
                            width: 0px                              
                        }}""")

        if isinstance(QLayoutType, QVBoxLayout) : # whats this for?
            self.myLayout = QLayoutType(self.container, alignment=Qt.AlignmentFlag.AlignCenter)
            QLayoutType.setContentsMargins(0,0,0,0) 
        else :
            self.myLayout = QLayoutType(self.container)
        parentWidget.addWidget(self)
    
    def addWidget(self, widget) :
        self.myLayout.addWidget(widget)
    
    def addStretch(self) :
        self.myLayout.addStretch()
    
    def addItem(self, item) :
        self.myLayout.addItem(item)
        self.myLayout.setContentsMargins(0,0,0,0)
        self.myLayout.setSpacing(0)

    def getLayout(self) :
        return self.myLayout


