from PyQt5.QtWidgets import QMainWindow,QApplication, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication, QMovie
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
import sys

#cargar diseño
class Examples(QMainWindow):
    def __init__(self):
        super(Examples, self).__init__()
        loadUi('examples.ui', self)

        print(self.minimize_bt, self.normal_bt, self.maximize_bt, self.close_bt, self.up_frame)

       
#Mostrar logos de ventana 
        self.minimize_bt.setIcon(QIcon("images/minimize.png"))
        self.normal_bt.setIcon(QIcon("images/minimize_2.png"))
        self.maximize_bt.setIcon(QIcon("images/maximize.png"))
        self.close_bt.setIcon(QIcon("images/exit.png"))
#Cargar Gifs 
    def setGif(self, ruta):
        self.movie = QMovie(ruta)
        self.example.setMovie(self.movie)
        # Ajustar el GIF al tamaño del QLabel
        self.movie.setScaledSize(self.example.size())
        self.movie.start()


#Boton Max-Min
        self.normal_bt.hide()
        self.click_Posicion = None 
        self.minimize_bt.clicked.connect(lambda: self.showMinimized())
        self.normal_bt.clicked.connect(self.control_normal_bt)
        self.maximize_bt.clicked.connect(self.control_maximize_bt)
        self.close_bt.clicked.connect(lambda: self.close())
        
#Elimimnar Barra de titulo
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#Modificar tamaño
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        #mover ventana
        self.up_frame.mouseMoveEvent = self.mover_ventana

    def control_normal_bt(self):
        self.showNormal()
        self.normal_bt.hide()
        self.maximize_bt.show()
         
    def control_maximize_bt(self):
        self.showMaximized()
        self.maximize_bt.hide()
        self.normal_bt.show()
##sizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
#mover ventana
    def mousePressEvent(self, event):
        self.click_Posicion = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized()==False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos()+ event.globalPos() - self.click_Posicion)
                self.click_Posicion = event.globalPos()
                event.accept()
        if event.globalPos().y()<= 5 or event.globalPos().x()<=5:
            self.showMaximized()
            self.maximize_bt.hide()
            self.normal_bt.show()
        else:
            self.showNormal()
            self.normal_bt.hide()
            self.maximize_bt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Examples()
    my_app.show()
    sys.exit(app.exec_())