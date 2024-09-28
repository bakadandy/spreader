import db_manager
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Настройка основного окна
        self.setWindowTitle('Тез оқу')
        self.setGeometry(100, 100, 300, 150)

        # Создание виджетов
        self.label_login = QLabel('Логин:')
        self.label_password = QLabel('Пароль:')

        self.text_login = QLineEdit(self)
        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.Password)  # Скрываем пароль

        self.button_login = QPushButton('Кіру', self)
        self.button_create_account = QPushButton('Аккаунт жасау', self)

        # Настройка расположения виджетов
        layout = QVBoxLayout()

        layout_login = QHBoxLayout()
        layout_login.addWidget(self.label_login)
        layout_login.addWidget(self.text_login)

        layout_password = QHBoxLayout()
        layout_password.addWidget(self.label_password)
        layout_password.addWidget(self.text_password)

        layout_buttons = QVBoxLayout()
        layout_buttons.addWidget(self.button_login)
        layout_buttons.addWidget(self.button_create_account)

        # Добавление в главный layout
        layout.addLayout(layout_login)
        layout.addLayout(layout_password)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

        # Настройка сигналов (связь кнопок с функциями)
        self.button_login.clicked.connect(self.handle_login)
        self.button_create_account.clicked.connect(self.handle_create_account)

    def handle_login(self):
        # Обработка события при нажатии кнопки "Войти"
        login = self.text_login.text()
        password = self.text_password.text()
        print(f'Осы логинмен: {login}, парольмен кіру: {password}')

    def handle_create_account(self):
        # Обработка события при нажатии кнопки "Создать аккаунт"
        print('Жаңа аккаунт жасау')

