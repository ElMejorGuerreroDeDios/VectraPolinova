import sys
import os
from PyQt5.QtWidgets import QApplication


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../interfaces/Select_exercise')))
from select_exercise import SelectExercise

def main():
    app = QApplication(sys.argv)
    menu_principal = SelectExercise()
    menu_principal.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()