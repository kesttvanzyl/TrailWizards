import sys, res
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
import string
import random
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi


class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("LoginPageUI.ui", self)
        self.loginButton.clicked.connect(self.login)
        self.toRegisterPageButton.clicked.connect(self.show_registration)

    def login(self):
        username = self.usernameCred.text()
        password = self.passwordCred.text()
        widget.setCurrentIndex(2)

    def show_registration(self):
        widget.setCurrentIndex(1)


class RegisterApp(QDialog):
    def __init__(self):
        super(RegisterApp, self).__init__()
        loadUi("RegisterPageUI.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.generatePasswordButton.clicked.connect(self.generatepassword)
        self.toLoginPageButton.clicked.connect(self.showloginpage)

    def register(self):
        userfullname = self.fullNameEntry.text()
        email = self.emailEntry.text()
        userentry = self.usernameRegisterEntry.text()
        passwordentry = self.passwordRegisterEntry.text()

    def generatepassword(self):
        length = 15
        upper = True
        lower = True
        digits = True
        punctuation = True
        white = False

        chars = ''

        if upper:
            chars = chars + string.ascii_uppercase
        if lower:
            chars = chars + string.ascii_lowercase
        if digits:
            chars = chars + string.digits
        if punctuation:
            chars = chars + string.punctuation
        if white:
            chars = chars + string.whitespace

        res = ''.join(random.choice(chars) for i in range(0, length))

        QMessageBox.information(self, "Password Generator Result", "Secure Password:  " + res + "\n Write down "
                                                                                                "password and "
                                                                                                "memorize it or keep "
                                                                                                "it in a secure "
                                                                                                "place.")


    def showloginpage(self):
        widget.setCurrentIndex(0)


class SchedulerApp(QDialog):
    def __init__(self):
        super(SchedulerApp, self).__init__()
        loadUi("SchedulerPageUI.ui", self)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
loginForm = LoginApp()
registrationForm = RegisterApp()
schedulerTable = SchedulerApp()
widget.addWidget(loginForm)
widget.addWidget(registrationForm)
widget.addWidget(schedulerTable)
widget.setCurrentIndex(0)
widget.setFixedWidth(1100)
widget.setFixedHeight(619)
widget.show()


app.exec_()
