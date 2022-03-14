import os
import sys
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QListView, QListWidgetItem
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon

LOCAL = os.path.dirname(os.path.abspath(__file__))

class ImageList(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallpaper- Gallery")
        

        self.listWidget = QListView()
        self.listWidget.setViewMode(QListView.IconMode)

        self.listWidget.setViewMode(QListView.IconMode)
        self.item = QListWidgetItem()
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap((f'{LOCAL}/Resources/gallery/BobbioItaly_EN-US7115321929.jpeg'))) #, QIcon.Normal, QIcon.Off))
        self.item.setIcon(self.icon)
        self.listWidget.addItem(self.item)


        # self.central_widget = QWidget()               
        # self.setCentralWidget(self.central_widget)    
        # lay = QVBoxLayout(self.central_widget)
        
        # label = QLabel(self)
        # pixmap = QPixmap(f'{LOCAL}/Resources/gallery/BobbioItaly_EN-US7115321929.jpeg')
        # label.setPixmap(pixmap)
        # self.resize(pixmap.width(), pixmap.height())
        
        # lay.addWidget(label)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageList()
    app.exec_()