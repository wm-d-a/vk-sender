import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
import vk_api

from PyQt5 import QtCore, QtGui, QtWidgets
import config
import time
import random


def my_filter(users):
    for i, item in enumerate(users):
        if '/' in item:
            # https://vk.com/self_ise
            users[i] = item.split('/')[-1]
    return users


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(572, 514)
        self.center()

        self.login = QtWidgets.QLineEdit(self)
        self.login.setPlaceholderText('Логин')
        self.login.setEnabled(True)
        self.login.setGeometry(QtCore.QRect(140, 30, 301, 41))
        self.login.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.login.setFrame(False)
        self.login.setAlignment(QtCore.Qt.AlignCenter)
        self.login.setObjectName("login")

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText('Пароль')
        self.password.setEnabled(True)
        self.password.setGeometry(QtCore.QRect(140, 90, 301, 41))
        self.password.setFrame(False)
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setObjectName("password")

        self.user_ids = QtWidgets.QTextEdit(self)
        self.user_ids.setPlaceholderText("ID user'ов")
        self.user_ids.setEnabled(True)
        self.user_ids.setGeometry(QtCore.QRect(140, 150, 301, 81))
        self.user_ids.setStyleSheet("border: none")
        self.user_ids.setObjectName("user_ids")
        self.user_ids.setAlignment(QtCore.Qt.AlignCenter)

        self.message = QtWidgets.QTextEdit(self)
        self.message.setEnabled(True)
        self.message.setGeometry(QtCore.QRect(140, 250, 301, 81))
        self.message.setStyleSheet("border: none")
        self.message.setObjectName("message")
        self.message.setPlaceholderText("Сообщение")

        self.send_message = QtWidgets.QPushButton(self)
        self.send_message.setText('Отправить')
        self.send_message.setEnabled(True)
        self.send_message.setGeometry(QtCore.QRect(140, 350, 301, 41))
        self.send_message.setStyleSheet("")
        self.send_message.setFlat(False)
        self.send_message.setObjectName("send_message")
        self.send_message.clicked.connect(self.button_is_clicked)


        self.logs = QtWidgets.QLabel(self)
        self.logs.setGeometry(QtCore.QRect(140, 410, 301, 55))
        self.logs.setText("")
        self.logs.setObjectName("logs")
        self.logs.setAlignment(QtCore.Qt.AlignCenter)

        self.setWindowTitle('VKAutoSender v1.0')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_is_clicked(self):
        login = self.login.text()
        password = self.password.text()
        users = self.user_ids.toPlainText().split('\n')
        message = self.message.toPlainText()
        session = vk_api.VkApi(login=str(config.login), password=str(config.password), app_id=2685278)  # KateMobile app
        session.auth()
        vk = session.get_api()
        users = my_filter(users)
        c = 0
        self.logs.setStyleSheet('background-color: white')
        for user in users:
            c += 1
            try:
                user_meta = vk.users.get(user_ids=[user])[0]
                # vk.messages.send(user_id=user_meta['id'], message=message, random_id=random.randint(0, 500))
                to_logs = f'{c}) Успешно отправлено пользователю: {user_meta["first_name"]} {user_meta["last_name"][0]}.'

                if len(to_logs) > 36:
                    for i in range(0, len(to_logs), 36):
                        to_logs = to_logs[:i] + '\n' + to_logs[i:]
                #self.logs.setText(to_logs)
            except Exception:
                self.logs.setText(f'{c}) Юзер {user} не найден. Сообщение не отправлено')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
