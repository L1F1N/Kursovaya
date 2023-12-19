from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3


class RegistrationWindow(QDialog):
    def __init__(self, login_window):
        super().__init__()

        self.setWindowTitle('Регистрация')

        self.login_window = login_window

        self.login_label = QLabel('Логин:')
        self.login_edit = QLineEdit(self)

        self.password_label = QLabel('Пароль:')
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_label = QLabel('Подтвердите пароль:')
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button = QPushButton('Зарегистрироваться', self)
        self.cancel_button = QPushButton('Отмена', self)

        self.register_button.clicked.connect(self.register_account)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_edit)
        layout.addWidget(self.register_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def register_account(self):
        username = self.login_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите все данные для регистрации.')
        elif password != confirm_password:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают.')
        elif self.is_username_taken(username):
            QMessageBox.warning(self, 'Ошибка', 'Логин уже занят. Пожалуйста, выберите другой логин.')
        else:
            self.add_account(username, password)
            QMessageBox.information(self, 'Успех', 'Аккаунт успешно зарегистрирован.')
            self.accept()

    def is_username_taken(self, username):
        # Проверка, занят ли логин
        with sqlite3.connect('accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
            return cursor.fetchone() is not None

    def add_account(self, username, password):
        # Добавление аккаунта в базу данных
        with sqlite3.connect('accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
        conn.commit()


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = RegistrationWindow(None)
    window.show()
    sys.exit(app.exec())
