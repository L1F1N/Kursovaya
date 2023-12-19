from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QDialog
import sqlite3
import csv
from add_menu_item_dialog import AddMenuItemDialog


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Работа с меню')
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Создаем таблицу для отображения меню
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Категория', 'Цена (руб)'])

        # Создаем элементы управления
        self.add_button = QPushButton('Добавить', self)
        self.delete_button = QPushButton('Удалить', self)
        self.sort_price_button = QPushButton('Сортировать по цене', self)
        self.sort_category_button = QPushButton('Сортировать по категории', self)
        self.sort_name_button = QPushButton('Сортировать по названию', self)
        self.export_button = QPushButton('Выгрузить данные', self)

        # Размещаем элементы на форме
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.sort_price_button)
        buttons_layout.addWidget(self.sort_category_button)
        buttons_layout.addWidget(self.sort_name_button)
        buttons_layout.addWidget(self.export_button)
        layout.addLayout(buttons_layout)

        # Подключаем обработчики событий
        self.add_button.clicked.connect(self.show_add_dialog)
        self.delete_button.clicked.connect(self.delete_menu_item)
        self.sort_price_button.clicked.connect(self.sort_by_price)
        self.sort_category_button.clicked.connect(self.sort_by_category)
        self.sort_name_button.clicked.connect(self.sort_by_name)
        self.export_button.clicked.connect(self.export_data)

        # Инициализация базы данных
        self.init_database()
        # Загружаем данные в таблицу
        self.load_data()

    def init_database(self):
        # Инициализация базы данных
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            # Создаем таблицу, если её нет
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT,
                    price REAL
                )
            ''')
        conn.commit()

    def load_data(self):
        # Загружаем данные из базы данных в таблицу
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_items')
            data = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)

    def show_add_dialog(self):
        dialog = AddMenuItemDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.add_menu_item(data)

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

            # Загружаем обновленные данные в таблицу
            self.load_data()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите все данные для блюда.')

    def delete_menu_item(self):
        # Удаление выбранного блюда из базы данных
        selected_row = self.table.currentRow()

        if selected_row != -1:
            item_id = self.table.item(selected_row, 0).text()
            with sqlite3.connect('Menu.db') as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM menu_items WHERE id = ?', (item_id,))
            conn.commit()

            # Загружаем обновленные данные в таблицу
            self.load_data()

    def sort_by_price(self):
        # Сортировка по цене
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_items ORDER BY price ASC')
            data = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)

    def sort_by_category(self):
        # Сортировка по категории
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_items ORDER BY category')
            data = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)

    def sort_by_name(self):
        # Сортировка по названию
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_items ORDER BY name')
            data = cursor.fetchall()

            self.table.setRowCount(0)

            for row_number, row_data in enumerate(data):
                self.table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table.setItem(row_number, column_number, item)

    def export_data(self):
        # Выгрузка данных из базы данных в txt файл с сортировкой
        with sqlite3.connect('Menu.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_items')
            data = cursor.fetchall()

        # Создаем текстовый файл для записи
        with open('exported_data.txt', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')

            # Записываем заголовок
            writer.writerow(['ID', 'Название', 'Категория', 'Цена (руб)'])

            # Определение порядка категорий
            category_order = [
                'Закуски', 'Салаты', 'Супы', 'Горячие блюда', 'Гарниры',
                'Десерты', 'Горячие напитки', 'Холодные напитки',
                'Сильно алкогольные напитки', 'Вина'
            ]

            # Группируем данные по категориям
            grouped_data = {category: [] for category in category_order}
            for row_data in data:
                category = row_data[2]
                if category in grouped_data:
                    grouped_data[category].append(row_data)

            # Записываем данные в порядке категорий и сортируем внутри каждой категории по алфавиту по названию
            for category in category_order:
                category_data = sorted(grouped_data[category], key=lambda x: x[1])
                writer.writerows(category_data)

        QMessageBox.information(self, 'Успех', 'Данные выгружены в файл exported_data.txt')


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())
