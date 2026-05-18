
from PyQt5.QtWidgets import QMainWindow, QApplication

import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon

# Configuración de rutas relativas al archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(BASE_DIR, 'select_exercise.ui')

# Importamos la clase Examples del archivo vecino local
from examples import Examples

class SelectExercise(QMainWindow):
    def __init__(self):
        super(SelectExercise, self).__init__()
        loadUi(UI_PATH, self)

        # Cargar iconos de la barra superior sin bordes
        self.minimize_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/minimize.png")))
        self.normal_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/minimize_2.png")))
        self.maximize_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/maximize.png")))
        self.close_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/exit.png")))

        # Cargar pixmaps desde la subcarpeta local 'exercises'
        self.label.setPixmap(QPixmap(os.path.join(BASE_DIR, "exercises/lagartijas.jpg")))
        self.label_2.setPixmap(QPixmap(os.path.join(BASE_DIR, "exercises/sentadillas.jpg")))
        self.label_3.setPixmap(QPixmap(os.path.join(BASE_DIR, "exercises/plancha.jpg")))
        self.label_4.setPixmap(QPixmap(os.path.join(BASE_DIR, "exercises/zancadas.jpg")))

        self.normal_bt.hide()
        self.click_Posicion = None

        self.minimize_bt.clicked.connect(lambda: self.showMinimized())
        self.normal_bt.clicked.connect(self.control_normal_bt)
        self.maximize_bt.clicked.connect(self.control_maximize_bt)
        self.close_bt.clicked.connect(lambda: self.close())

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        self.up_frame.mouseMoveEvent = self.mover_ventana

        # Inicializar ventana secundaria de ejemplos
        self.example_window = Examples()

        # Enlace de botones enviando las rutas absolutas de los GIFs locales y su identificador
        self.exercise_bt_1.clicked.connect(lambda: self.abrir_ejemplo("exercises/lagartijas.gif", "Lagartija"))
        self.exercise_bt_2.clicked.connect(lambda: self.abrir_ejemplo("exercises/sentadilla.gif", "Sentadilla"))
        self.exercise_bt_3.clicked.connect(lambda: self.abrir_ejemplo("exercises/plancha.gif", "Plancha"))
        self.exercise_bt_4.clicked.connect(lambda: self.abrir_ejemplo("exercises/zancada.gif", "Zancada"))

    def abrir_ejemplo(self, path_relativo_gif, nombre_ejercicio):
        ruta_absoluta_gif = os.path.join(BASE_DIR, path_relativo_gif)
        self.example_window.setGif(ruta_absoluta_gif, nombre_ejercicio)
        self.example_window.show()

    def control_normal_bt(self):
        self.showNormal()
        self.normal_bt.hide()
        self.maximize_bt.show()

    def control_maximize_bt(self):
        self.showMaximized()
        self.maximize_bt.hide()
        self.normal_bt.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_Posicion = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_Posicion)
                self.click_Posicion = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.maximize_bt.hide()
            self.normal_bt.show()
        else:
            self.showNormal()
            self.normal_bt.hide()
            self.maximize_bt.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = SelectExercise()
    window.show()
    sys.exit(app.exec_())

"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout
>>>>>>> a62c1a4d397386ce0c23ad180753ce108fc2d451
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys
import os
# Cargar examples.ui
class Examples(QMainWindow):
    def __init__(self):
        super(Examples, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "examples.ui") #Esto busca el archivo utilizando rutas relativas 
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

    def setGif(self, ruta):
        gif_path = os.path.join(os.path.dirname(__file__), ruta)
        self.movie = QMovie(gif_path)
        self.example.setMovie(self.movie)
        self.movie.start()

    def open_exercise(self):
        self.start_bt.setStyleSheet(
        "QPushButton { background-color: red; color: white; }" #Esto se cambiará por una funciñon para abrir  el ejercicio correspondiente
        )

#cargar diseño
class SelectExercise(QMainWindow):
    def __init__(self):
        super(SelectExercise, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "select_exercise.ui")
        loadUi(ui_path, self)
        

#Mostrar logos de ventana 
        self.minimize_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/minimize.png")))#Esto busca el archivo utilizando rutas relativas
        self.normal_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/minimize_2.png")))
        self.maximize_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/maximize.png")))
        self.close_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/exit.png")))

        self.label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"exercises/lagartijas.jpg")))#Esto busca el archivo utilizando rutas relativas
        self.label_2.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"exercises/sentadillas.jpg")))
        self.label_3.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"exercises/plancha.jpg")))
        self.label_4.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"exercises/zancadas.jpg")))

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
"""