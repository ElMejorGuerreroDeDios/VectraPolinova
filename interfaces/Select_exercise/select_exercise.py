from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys

# Cargar examples.ui
class Examples(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana GIF")
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.movie = None

    def setGif(self, ruta):
        self.movie = QMovie(ruta)
        self.label.setMovie(self.movie)
        self.movie.start()


#cargar diseño
class SelectExercise(QMainWindow):
    def __init__(self):
        super(SelectExercise, self).__init__()
        loadUi('select_exercise.ui', self)
       
#Mostrar logos de ventana 
        self.minimize_bt.setIcon(QIcon("images/minimize.png"))
        self.normal_bt.setIcon(QIcon("images/minimize_2.png"))
        self.maximize_bt.setIcon(QIcon("images/maximize.png"))
        self.close_bt.setIcon(QIcon("images/exit.png"))

        self.label.setPixmap(QPixmap("exercises/lagartijas.jpg"))
        self.label_2.setPixmap(QPixmap("exercises/sentadillas.jpg"))
        self.label_3.setPixmap(QPixmap("exercises/plancha.jpg"))
        self.label_4.setPixmap(QPixmap("exercises/zancadas.jpg"))

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

        # Crear la ventana de examples
        self.example = Examples()

        # conectar botones de select a examples
        self.exercise_bt_1.clicked.connect(lambda: self.showExample("exercises/lagartijas.gif"))
        self.exercise_bt_2.clicked.connect(lambda: self.showExample("exercises/sentadilla.gif"))
        self.exercise_bt_3.clicked.connect(lambda: self.showExample("exercises/plancha.gif"))
        self.exercise_bt_4.clicked.connect(lambda: self.showExample("exercises/zancada.gif"))

    def showExample(self, ruta):
        self.example.setGif(ruta)
        self.example.show()

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
    my_app = SelectExercise()
    my_app.show()
    sys.exit(app.exec_())