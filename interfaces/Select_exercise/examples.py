from PyQt5.QtWidgets import QMainWindow,QApplication, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication, QMovie
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
import sys
import os

#cargar diseño
class Examples(QMainWindow):
    def __init__(self):
        super(Examples, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "examples.ui")
        loadUi(ui_path, self)

    
#Mostrar logos de ventana 
        base_path = os.path.dirname(__file__)
        self.minimize_bt.setIcon(QIcon(os.path.join(base_path, "images/minimize.png"))) #Esto busca el archivo utilizando rutas relativas
        self.normal_bt.setIcon(QIcon(os.path.join(base_path, "images/minimize_2.png")))
        self.maximize_bt.setIcon(QIcon(os.path.join(base_path, "images/maximize.png")))
        self.close_bt.setIcon(QIcon(os.path.join(base_path, "images/exit.png")))



#Boton Max-Min
        self.normal_bt.hide()
        self.click_Posicion = None 
        self.minimize_bt.clicked.connect(lambda: self.showMinimized())
        self.normal_bt.clicked.connect(self.control_normal_bt)
        self.maximize_bt.clicked.connect(self.control_maximize_bt)
        self.close_bt.clicked.connect(lambda: self.close())

                #Boton para iniciar el ejercicio
        self.start_bt.clicked.connect(self.open_exercise)

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

#Cargar Gifs 
    def setGif(self, ruta):
        gif_path = os.path.join(os.path.dirname(__file__), ruta)
        self.movie = QMovie(gif_path)
        self.example.setMovie(self.movie)   # QLabel llamado "example" en el .ui
        self.movie.setScaledSize(self.example.size())
        self.movie.start()
        


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

    def open_exercise(self):
        self.start_bt.setStyleSheet(
            "QPushButton { background-color: red; color: white; }" #Esto se cambiará por una funciñon para abrir  el ejercicio correspondiente
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Examples()
    my_app.show()
    sys.exit(app.exec_())