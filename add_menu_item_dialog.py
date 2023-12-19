from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout
import sqlite3


class AddMenuItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Добавить блюдо')

        self.name_label = QLabel('Название:')
        self.name_edit = QLineEdit(self)

        self.category_label = QLabel('Категория:')
        self.category_combo = QComboBox(self)
        self.category_combo.addItems(['Закуски', 'Салаты', 'Супы', 'Горячие блюда', 'Гарниры', 'Десерты',
                                      'Горячие напитки', 'Холодные напитки', 'Сильно алкогольные напитки', 'Вина'])

        self.price_label = QLabel('Цена (руб):')
        self.price_edit = QLineEdit(self)

        self.add_button = QPushButton('Добавить', self)
        self.cancel_button = QPushButton('Отмена', self)

        self.add_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_edit)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_data(self):
        return {
            'name': self.name_edit.text(),
            'category': self.category_combo.currentText(),
            'price': self.price_edit.text(),
        }

    def accept(self):
        data = self.get_data()
        self.add_menu_item(data)
        super().accept()

    def add_menu_item(self, data):
        # Добавление нового блюда в базу данных
        name = data['name']
        category = data['category']
        price = data['price']

        if name and category and price:
            with sqlite3.connect('Menu.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)', (name, category, price))
            conn.commit()


if __name__ == '__main__':
    dialog = AddMenuItemDialog()
    dialog.exec()
