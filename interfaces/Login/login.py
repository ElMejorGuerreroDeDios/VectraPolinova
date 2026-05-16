from PyQt5.QtWidgets import QMainWindow,QApplication, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
import sys
import os

#cargar ui de register
class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__),"register.ui") #Esto busca el archivo utilizando rutas relativas
        loadUi(ui_path, self)
        #ocultar contraseña(ininicio)
        self.password.setEchoMode(QLineEdit.Password)

#cargar diseño
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        ui_path2 = os.path.join(os.path.dirname(__file__), "login.ui")
        loadUi(ui_path2, self)       
#ocultar contraseña(ininicio)
        self.password.setEchoMode(QLineEdit.Password)
        
#Mostrar imagen de perfil de usuario
        self.user_logo.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__),"images/user.png")))
        self.user_logo.setScaledContents(True)

#Mostrar logos de ventana 
        self.minimize_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/minimize.png"))) #Esto busca el archivo utilizando rutas relativas
        self.minimize_bt_2.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/minimize_2.png")))
        self.maximize_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/maximize.png")))
        self.close_bt.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/exit.png")))

#Boton Max-Min
        self.minimize_bt_2.hide()
        self.click_Posicion = None
        self.minimize_bt.clicked.connect(lambda: self.showMinimized())
        self.minimize_bt_2.clicked.connect(self.control_normal_bt)
        self.maximize_bt.clicked.connect(self.control_maximize_bt)
        self.close_bt.clicked.connect(lambda: self.close())
        

#Visualizar Contraseña
        self.show_pass_cb.toggled.connect(
    lambda checked: self.password.setEchoMode(
        QLineEdit.Normal if checked else QLineEdit.Password
    )
)
        #Abrir ventana de registro al presionar "Registrate"
        self.register_button.clicked.connect(self.open_register_window)

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
        self.minimize_bt_2.hide()
        self.maximize_bt.show()
         
    def control_maximize_bt(self):
        self.showMaximized()
        self.maximize_bt.hide()
        self.minimize_bt_2.show()
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
            self.minimize_bt_2.show()
        else:
            self.showNormal()
            self.minimize_bt_2.hide()
            self.maximize_bt.show()

        

    def open_register_window(self):
        self.register_window = Register()   # crea instancia de la ventana de registro
        self.register_window.show()         # muestra la ventana
        self.close()                        # opcional: cierra la ventana de login


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Login()
    my_app.show()
    sys.exit(app.exec_())