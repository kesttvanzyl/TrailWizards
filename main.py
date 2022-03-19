import sys, res
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
import string
import random
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import zmq
import pyclip
from time import sleep

""" A socket publisher and subscriber """
# setting up a sending side to request a service
# context variable
context = zmq.Context()
# setup the socket
socket_snd = context.socket(zmq.PUB)
# bind it to a socket, local this time, set to what ever you want to use
socket_snd.bind('tcp://127.0.0.1:2001')  # local port for testing

#  set up the socket to connect to the port for rec the reply
socket_rec = context.socket(zmq.SUB)
# connect the socket to the port (same as in the publisher)
socket_rec.connect('tcp://127.0.0.1:2000')

# setting up the socket option and listen
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

credentials_dict = {}


class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi("LoginPageUI.ui", self)
        self.loginButton.clicked.connect(self.login)
        self.toRegisterPageButton.clicked.connect(self.show_registration)

    def login(self):
        username = self.usernameCred.text()
        password = self.passwordCred.text()
        if username in credentials_dict:
            password_cred = credentials_dict[username]
            if password_cred == password:
                widget.setCurrentIndex(2)
            else:
                QMessageBox.information(self, "Whoops!",
                                        "Incorrect password. Please try again.")

        else:
            QMessageBox.information(self, "Whoops!", "Username not found. Please try again. \n If you are not a member "
                                                     "yet, make sure to Register before trying to Login.")

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
        credentials_dict[userentry] = passwordentry
        widget.setCurrentIndex(0)

    def generatepassword(self):

        while True:
            message = "password()"
            # quit the test program
            if message == "quit":
                return
            # send the message to the TCP port
            print("Going to send this message: ", message)
            socket_snd.send_pyobj(message)
            print('sent message:', message)
            # setting up the received message
            message_ret = socket_rec.recv_pyobj()
            print("Returned message:", message_ret)
            pyclip.copy(message_ret)
            QMessageBox.information(self, "Password Generator Result", "Secure Password:  " + message_ret +
                                    "\n Your password has automatically been copied to your clipboard. Paste your new "
                                    "password in the password entry box.")
            break

    def showloginpage(self):
        widget.setCurrentIndex(0)


class SchedulerApp(QDialog):
    def __init__(self):
        super(SchedulerApp, self).__init__()
        loadUi("SchedulerPageUI.ui", self)
        self.logoutButton.clicked.connect(self.showloginpage)

    def showloginpage(self):
        widget.setCurrentIndex(0)


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
