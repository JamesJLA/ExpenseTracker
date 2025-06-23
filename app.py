# App Design
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout,
                             QMessageBox, QTableWidgetItem, QHeaderView, QHBoxLayout)

from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.setGeometry(300, 100, 550, 500)
        self.setWindowTitle('Expense Tracker App')

    # Design
    def initUI(self):
        # Create all Objects
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton('Add Expense')
        self.btn_add.setObjectName('btn_add')
        self.btn_delete = QPushButton('Delete Expense')
        self.btn_delete.setObjectName('btn_delete')

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expenses)

        self.apply_styles()
        # add widgets to a layout(Row/ Column)
        self.setup_layout()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel('Date'))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel('Category'))
        row1.addWidget(self.dropdown)

        # Row 2
        row2.addWidget(QLabel('Amount'))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel('Description'))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    def apply_styles(self):
        self.setStyleSheet('''
            QWidget {
                background-color: #e3e9f2;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }

            QLabel {
                font-size: 16px;
                color: #2c3e50;
                font-weight: bold;
                padding: 5px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #fff;
                font-size: 14px;
                color: #333;
                border: 1px solid #b0bfc6;
                border-radius: 0px;
                padding: 5px;
            }

            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #2a9d8f;
                background-color: #f5f9fc;
            }
            
            #btn_add {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }

            #btn_add:hover {
                background-color: #2980b9;
            }
            
            #btn_add:pressed {
                background-color: #1c6692;
            }
            
            #btn_delete {
                background-color: #ff102e;
                color: white;
                border: none;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }

            #btn_delete:hover {
                background-color: #b20b20;
            }
            
            #btn_delete:pressed {
                background-color: #ff102e;
            }

            QTableWidget {
                background-color: #fff;
                alternate-background-color: #f2f7fb;
                gridline-color: #c0c9d0;
                selection-background-color: #4caf50;
                selection-color: white;
                font-size: 14px;
                border: 1px solid #cfd9e1;
            }
        ''')


    def populate_dropdown(self):
        categories = ['Food', 'Entertainment', 'Shopping', 'Other']
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()


    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText() #QComboBox
        amount = self.amount.text() #QLineEdit
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty")
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Could not Add Expense")

    def delete_expenses(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Uh Oh", "You Need To Choose a Row to Delete")
            return

        expense_id = int (self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to Delete this Expense?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()