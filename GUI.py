import time

from PyQt5.QtCore import QTimer

import db_manager
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QFileDialog, QMessageBox


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = db_manager.DBManager()
        self.init_ui()

    def __del__(self):
        del self.db
    def init_ui(self):
        # Настройка основного окна
        self.setWindowTitle('Тез оқу')
        self.setGeometry(100, 100, 300, 150)

        # Создание виджетов
        self.label_login = QLabel('Логин:')
        self.label_password = QLabel('Пароль:')
        self.label_info = QLabel(' ')

        self.text_login = QLineEdit(self)
        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.Password)  # Скрываем пароль

        self.button_login = QPushButton('Кіру', self)
        self.button_create_account = QPushButton('Аккаунт жасау', self)

        # Настройка расположения виджетов
        layout = QVBoxLayout()

        layout_info = QHBoxLayout()
        layout.addWidget(self.label_info)

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
        if login.strip() == "" or password.strip() == "":
            self.label_info.setText("Аккауттың атын немесе құпиясөзін еңгізіңіз")
            return
        answer = self.db.login_check(login, password)
        self.label_info.setText(answer)
        if answer == "Тіркелу орындалды":
            print(f'Осы логинмен: {login}, парольмен кіру: {password}')
            self.show_TypingSpeedTest()

    def handle_create_account(self):
        # Обработка события при нажатии кнопки "Создать аккаунт"
        login = self.text_login.text()
        password = self.text_password.text()
        if login.strip() == "" or password.strip() == "":
            self.label_info.setText("Аккауттың атын немесе құпиясөзін еңгізіңіз")
            return
        self.label_info.setText(self.db.add_user(login, password))
        print('Жаңа аккаунт жасау')
    def show_TypingSpeedTest(self):
        self.typingspeedtest = TypingSpeedTest()
        self.typingspeedtest.show()
        self.close()

class TypingSpeedTest(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Timer for calculating words per minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.start_time = 0
        self.is_running = False

    def init_ui(self):
        self.setWindowTitle('Typing Speed Test')

        # Text editor
        self.text_edit = QTextEdit(self)

        # Buttons
        self.open_file_button = QPushButton('Открыть Файл')
        self.copy_clipboard_button = QPushButton('Скопировать текст из буфера')
        self.start_button = QPushButton('Старт')
        self.stop_button = QPushButton('Стоп')

        # Connect buttons to functions
        self.open_file_button.clicked.connect(self.open_file)
        self.copy_clipboard_button.clicked.connect(self.copy_from_clipboard)
        self.start_button.clicked.connect(self.start_test)
        self.stop_button.clicked.connect(self.stop_test)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_file_button)
        button_layout.addWidget(self.copy_clipboard_button)

        start_stop_layout = QHBoxLayout()
        start_stop_layout.addWidget(self.start_button)
        start_stop_layout.addWidget(self.stop_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.text_edit)
        layout.addLayout(start_stop_layout)

        self.setLayout(layout)

    def open_file(self):
        # Open file dialog to select a file and load its content into the text editor
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.text_edit.setPlainText(file.read())

    def copy_from_clipboard(self):
        # Copy text from the system clipboard to the text editor
        clipboard = QApplication.clipboard()
        self.text_edit.setPlainText(clipboard.text())

    def start_test(self):
        # Start the timer for the typing test
        self.text_edit.setReadOnly(False)  # Allow typing
        self.text_edit.clear()  # Clear any pre-existing text
        self.start_time = time.time()
        self.is_running = True
        self.timer.start(1000)  # Update timer every second

    def stop_test(self):
        if not self.is_running:
            return

        self.timer.stop()
        elapsed_time = time.time() - self.start_time
        text = self.text_edit.toPlainText()
        word_count = len(text.split())

        # Calculate words per minute (WPM)
        wpm = (word_count / elapsed_time) * 60
        self.show_result(wpm)
        self.is_running = False

    def update_time(self):
        pass  # Update timer display if necessary

    def show_result(self, wpm):
        # Display a message box with the WPM result
        msg = QMessageBox()
        msg.setWindowTitle("Результат")
        msg.setText(f"Ваш результат составил {wpm:.2f} слов/мин")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Yes)
        msg.exec_()