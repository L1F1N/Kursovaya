from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
from registration_window import RegistrationWindow
from menu_window import MenuWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Авторизация')

        self.login_label = QLabel('Логин:')
        self.login_edit = QLineEdit(self)

        self.password_label = QLabel('Пароль:')
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Войти', self)
        self.login_button.clicked.connect(self.show_menu_window)

        self.register_button = QPushButton('Зарегистрироваться', self)
        self.register_button.clicked.connect(self.show_registration_window)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def show_menu_window(self):
        username = self.login_edit.text()
        password = self.password_edit.text()
        if username and password and self.is_valid_password(username, password):
            self.menu_window = MenuWindow()
            self.menu_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неправильный логин или пароль.')

    def show_registration_window(self):
        self.registration_window = RegistrationWindow(self)  # Передаем ссылку на LoginWindow
        self.registration_window.show()

    def is_valid_password(self, username, password):
        # Проверка пароля в базе данных
        with sqlite3.connect('accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
            return cursor.fetchone() is not None


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
