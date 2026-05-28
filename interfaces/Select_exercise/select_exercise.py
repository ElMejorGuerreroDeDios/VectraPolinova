import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(BASE_DIR, 'select_exercise.ui')

from examples import Examples

class SelectExercise(QMainWindow):
    def __init__(self):
        super(SelectExercise, self).__init__()
        loadUi(UI_PATH, self)

        self.minimize_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/minimize.png")))
        self.normal_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/minimize_2.png")))
        self.maximize_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/maximize.png")))
        self.close_bt.setIcon(QIcon(os.path.join(BASE_DIR, "images/exit.png")))

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

        self._example_window = None

        self.exercise_bt_1.clicked.connect(lambda: self.abrir_ejemplo("exercises/lagartijas.gif", "Lagartija"))
        self.exercise_bt_2.clicked.connect(lambda: self.abrir_ejemplo("exercises/sentadilla.gif", "Sentadilla"))
        self.exercise_bt_3.clicked.connect(lambda: self.abrir_ejemplo("exercises/plancha.gif", "Plancha"))
        self.exercise_bt_4.clicked.connect(lambda: self.abrir_ejemplo("exercises/zancada.gif", "Zancada"))

    def abrir_ejemplo(self, path_relativo_gif, nombre_ejercicio):

        if self._example_window is not None:
            self._example_window.close()
            self._example_window = None

        ruta_absoluta_gif = os.path.join(BASE_DIR, path_relativo_gif)
        self._example_window = Examples(nombre_ejercicio)
        self._example_window.setGif(ruta_absoluta_gif, nombre_ejercicio)
        self._example_window.show()

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