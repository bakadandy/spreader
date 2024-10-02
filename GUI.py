import time
import db_manager

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QFileDialog, QMessageBox, QLCDNumber)


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
            self.show_chooseWindow()

    def handle_create_account(self):
        # Обработка события при нажатии кнопки "Создать аккаунт"
        login = self.text_login.text()
        password = self.text_password.text()
        if login.strip() == "" or password.strip() == "":
            self.label_info.setText("Аккауттың атын немесе құпиясөзін еңгізіңіз")
            return
        self.label_info.setText(self.db.add_user(login, password))
        print('Жаңа аккаунт жасау')

    def show_chooseWindow(self):
        self.hide()
        self.chooseWindow = chooseWindow(self)
        self.chooseWindow.show()

class chooseWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Мәзір')
        self.setGeometry(100, 100, 300, 100)

        # Buttons for training and testing sections
        self.training_button = QPushButton('Жаттығу аймағы')
        self.testing_button = QPushButton('Тестілеу аймағы')
        self.logout_button = QPushButton('Аккаунтан шығу')

        # Connect buttons to functions
        self.training_button.clicked.connect(self.open_training_section)
        self.testing_button.clicked.connect(self.open_testing_section)
        self.logout_button.clicked.connect(self.logout)

        # Layout for training and testing buttons and LCD
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.training_button)
        button_layout.addWidget(self.testing_button)

        logout_layout = QHBoxLayout()
        logout_layout.addWidget(self.logout_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addLayout(logout_layout)

        self.setLayout(layout)

    def open_training_section(self):
        # Open the RSVPDialog window for training
        self.hide()
        self.training_window = RSVPDialog(self)
        self.training_window.show()

    def open_testing_section(self):
        # Open the TestDialog window for testing
        self.hide()
        self.testing_window = TypingSpeedTest(self)
        self.testing_window.show()

    def logout(self):
        self.hide()
        self.parent.show()


class TypingSpeedTest(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

        # Timer for calculating words per minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_time = 0
        self.is_running = False

        self.elapsed_time = 0

    def init_ui(self):
        self.setWindowTitle('Тестілеу аймағы')
        self.setGeometry(100, 100, 400, 800)

        # Text editor
        self.text_edit = QTextEdit(self)

        #LCD
        self.lcd = QLCDNumber(self)
        self.lcd.display('00:00')
        self.lcd.setDigitCount(9)
        self.lcd.setFixedSize(300, 100)

        # Buttons
        self.open_file_button = QPushButton('Файлды ашу')
        self.copy_clipboard_button = QPushButton('Буфердан текстты көшіру')
        self.start_button = QPushButton('Бастау')
        self.stop_button = QPushButton('Аяқтау')
        self.back_btn = QPushButton('Артқа')

        # Connect buttons to functions
        self.open_file_button.clicked.connect(self.open_file)
        self.copy_clipboard_button.clicked.connect(self.copy_from_clipboard)
        self.start_button.clicked.connect(self.start_test)
        self.stop_button.clicked.connect(self.stop_test)
        self.back_btn.clicked.connect(self.go_back)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_file_button)
        button_layout.addWidget(self.copy_clipboard_button)

        start_stop_layout = QHBoxLayout()
        start_stop_layout.addWidget(self.start_button)
        start_stop_layout.addWidget(self.lcd)
        start_stop_layout.addWidget(self.stop_button)
        start_stop_layout.addWidget(self.back_btn)

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
        self.text_edit.setReadOnly(True)  # Allow typing
        self.start_time = time.time()
        self.is_running = True
        self.timer.start(1)  # Update timer every second
        self.start_button.setEnabled(False)  # Disable start button while timer is running
        self.stop_button.setEnabled(True)

    def stop_test(self):
        self.timer.stop()
        elapsed_time = time.time() - self.start_time
        text = self.text_edit.toPlainText()
        word_count = len(text.split())

        # Calculate words per minute (WPM)
        wpm = (word_count / elapsed_time) * 60
        self.show_result(wpm)
        self.is_running = False
        self.elapsed_time = 0  # Reset elapsed time
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_timer(self):
        self.elapsed_time += 1  # Increment elapsed time
        minutes = (self.elapsed_time // 60000) % 60  # Calculate minutes
        seconds = (self.elapsed_time // 1000) % 60  # Calculate seconds
        milliseconds = self.elapsed_time % 1000  # Calculate milliseconds

        # Format time as mm:ss:msms
        formatted_time = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
        self.lcd.display(formatted_time)

    def show_result(self, wpm):
        # Display a message box with the WPM result
        msg = QMessageBox()
        msg.setWindowTitle("Қорытынды")
        msg.setText(f"Сіздің қорытынды {wpm:.2f} сөз/мин")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Yes)
        msg.exec_()

    def go_back(self):
        self.timer.stop()
        self.hide()
        self.parent.show()


class RSVPDialog(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # Set window properties
        self.setWindowTitle('Жаттығу аймағы')
        self.setGeometry(100, 100, 400, 300)

        # Layout setup
        layout = QtWidgets.QVBoxLayout()

        # Input line edit for RSVP word display
        self.word_display = QtWidgets.QLineEdit(self)
        self.word_display.setAlignment(Qt.AlignCenter)
        self.word_display.setReadOnly(True)
        layout.addWidget(self.word_display)

        # Slider for progress
        self.progress_slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.progress_slider.setMinimum(0)
        layout.addWidget(self.progress_slider)

        # Speed setting layout (includes QLabel and QSpinBox)
        speed_layout = QtWidgets.QHBoxLayout()
        speed_label = QtWidgets.QLabel("Жылдамдық (сөз/мин):")
        speed_layout.addWidget(speed_label)

        self.speed_spin_box = QtWidgets.QSpinBox(self)
        self.speed_spin_box.setRange(10, 1000)  # Min 10 WPM, Max 1000 WPM
        self.speed_spin_box.setValue(200)  # Default speed
        speed_layout.addWidget(self.speed_spin_box)
        layout.addLayout(speed_layout)

        # Text area for input
        self.text_area = QtWidgets.QTextEdit(self)
        layout.addWidget(self.text_area)

        # Buttons for starting and pausing
        button_layout = QtWidgets.QHBoxLayout()

        self.start_button = QtWidgets.QPushButton('Бастау', self)
        button_layout.addWidget(self.start_button)

        self.pause_button = QtWidgets.QPushButton('Пауза', self)
        button_layout.addWidget(self.pause_button)

        self.back_btn = QtWidgets.QPushButton('Артқа', self)
        button_layout.addWidget(self.back_btn)

        layout.addLayout(button_layout)

        # Set main layout
        self.setLayout(layout)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_rsvp)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.back_btn.clicked.connect(self.go_back)

        # Timer setup for word display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_word)
        self.words = []
        self.current_word_index = 0
        self.is_paused = False

    def start_rsvp(self):
        text = self.text_area.toPlainText()
        if text:
            self.words = text.split()
            self.current_word_index = 0
            self.progress_slider.setMaximum(len(self.words) - 1)

            # Get speed value from spin box (WPM)
            interval = 60000 // self.speed_spin_box.value()  # Speed in milliseconds per word
            self.timer.start(interval)
            self.update_word()

    def toggle_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText('Жалғастыру')
        else:
            if self.words:
                interval = 60000 // self.speed_spin_box.value()
                self.timer.start(interval)
                self.pause_button.setText('Пауза')

    def update_word(self):
        if self.current_word_index < len(self.words):
            # Update the displayed word
            self.word_display.setText(self.words[self.current_word_index])

            # Move the progress slider to show reading progress
            self.progress_slider.setValue(self.current_word_index)

            # Increment the index to the next word
            self.current_word_index += 1
        else:
            # Stop the timer when we reach the end of the text
            self.timer.stop()

    def go_back(self):
        self.timer.stop()
        self.hide()
        self.parent.show()