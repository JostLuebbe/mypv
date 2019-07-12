from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QLineEdit, QApplication
from api import create_user, check_password, get_services, get_user, add_service, get_password
from pathlib import Path


class CreateAccountWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create Account')
        icon_path = Path.cwd() / 'resources' / 'images' / 'padlock.png'
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        self.username_label = QtWidgets.QLabel('Username:')
        self.username_field = QtWidgets.QLineEdit()

        self.password_label = QtWidgets.QLabel('Password:')
        self.password_field = QtWidgets.QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QtWidgets.QLabel('Confirm Password:')
        self.confirm_password_field = QtWidgets.QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.Password)

        self.create_account_button = QtWidgets.QPushButton('Create Account')

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.username_label, 0, 0)
        self.layout.addWidget(self.username_field, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.password_field, 1, 1)
        self.layout.addWidget(self.confirm_password_label, 2, 0)
        self.layout.addWidget(self.confirm_password_field, 2, 1)
        self.layout.addWidget(self.create_account_button, 3, 0, 2, 0)
        self.setLayout(self.layout)

        self.create_account_button.clicked.connect(self.create_account)

    def create_account(self):
        if self.password_field.text() == self.confirm_password_field.text():
            create_user(self.username_field.text(), self.password_field.text())
            self.close()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Your password fields don\'t match!')


class AddServiceWindow(QtWidgets.QWidget):

    new_service_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Service')
        icon_path = Path.cwd() / 'resources' / 'images' / 'padlock.png'
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        self.user = None

        self.service_name_label = QtWidgets.QLabel('Service Name:')
        self.service_name_field = QtWidgets.QLineEdit()

        self.service_username_label = QtWidgets.QLabel('Service Username:')
        self.service_username_field = QtWidgets.QLineEdit()

        self.service_password_label = QtWidgets.QLabel('Service Password:')
        self.service_password_field = QtWidgets.QLineEdit()
        self.service_password_field.setEchoMode(QLineEdit.Password)

        self.confirm_service_password_label = QtWidgets.QLabel('Confirm Service Password:')
        self.confirm_service_password_field = QtWidgets.QLineEdit()
        self.confirm_service_password_field.setEchoMode(QLineEdit.Password)

        self.submit_button = QtWidgets.QPushButton('Submit')
        self.submit_button.clicked.connect(self.add_service_action)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.service_name_label, 0, 0)
        self.layout.addWidget(self.service_name_field, 0, 1)
        self.layout.addWidget(self.service_username_label, 1, 0)
        self.layout.addWidget(self.service_username_field, 1, 1)
        self.layout.addWidget(self.service_password_label, 2, 0)
        self.layout.addWidget(self.service_password_field, 2, 1)
        self.layout.addWidget(self.confirm_service_password_label, 3, 0)
        self.layout.addWidget(self.confirm_service_password_field, 3, 1)
        self.layout.addWidget(self.submit_button, 4, 0, 1, 2)
        self.setLayout(self.layout)

    def add_service_action(self):
        if self.service_password_field.text() == self.confirm_service_password_field.text():
            add_service(
                self.user,
                self.service_name_field.text(),
                self.service_username_field.text(),
                self.service_password_field.text()
            )
            self.new_service_signal.emit()
            self.close()


class ServicesWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Services')
        icon_path = Path.cwd() / 'resources' / 'images' / 'padlock.png'
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        stylesheet_path = Path.cwd() / 'resources' / 'stylesheets' / 'services_window.css'
        with open(stylesheet_path) as f:
            self.setStyleSheet(f.read())

        self.user = None

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.services_layout = QtWidgets.QVBoxLayout()
        self.services_layout.setSpacing(0)

        self.layout.addLayout(self.services_layout)

        self.update_service_list()

        self.add_service_button = QtWidgets.QPushButton('Add Service')
        self.add_service_button.clicked.connect(self.add_service)
        self.layout.addWidget(self.add_service_button)

        self.add_service_window = AddServiceWindow()
        self.add_service_window.new_service_signal.connect(self.update_service_list)

        self.setLayout(self.layout)

    def update_service_list(self):
        while self.services_layout.count():
            child = self.services_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        services = get_services()

        for service in services:
            service_button = QtWidgets.QPushButton(service.service_name)
            service_button.setObjectName('service_button')
            print(service_button.text())
            service_button.clicked.connect(lambda: self.get_password(service_button.text()))
            self.services_layout.addWidget(service_button)

    def get_password(self, service_name):
        print(service_name)
        QApplication.clipboard().setText(get_password(self.user, service_name))

    def add_service(self):
        self.add_service_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.add_service_window.user = self.user
        self.setDisabled(True)
        self.add_service_window.show()
        self.setDisabled(False)


class LoginWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        icon_path = Path.cwd() / 'resources' / 'images' / 'padlock.png'
        self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        self.user = None

        self.username_label = QtWidgets.QLabel('Username:')
        self.username_field = QtWidgets.QLineEdit()

        self.password_label = QtWidgets.QLabel('Password:')
        self.password_field = QtWidgets.QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton('Login')
        self.create_account_button = QtWidgets.QPushButton('Create Account')

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.username_label, 0, 0)
        self.layout.addWidget(self.username_field, 0, 1)
        self.layout.addWidget(self.password_label, 1, 0)
        self.layout.addWidget(self.password_field, 1, 1)
        self.layout.addWidget(self.login_button, 2, 0, 1, 2)
        self.layout.addWidget(self.create_account_button, 3, 0, 1, 2)
        self.setLayout(self.layout)

        self.login_button.clicked.connect(self.login)
        self.create_account_button.clicked.connect(self.create_account)
        self.services_window = ServicesWindow()
        self.create_account_window = CreateAccountWindow()

    def login(self):
        if check_password(self.username_field.text(), self.password_field.text()):
            self.user = get_user(self.username_field.text())
            self.services_window.user = self.user
            self.hide()
            self.services_window.show()

    def create_account(self):
        self.create_account_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setDisabled(True)
        self.create_account_window.show()
        self.setDisabled(False)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
            self.login()

