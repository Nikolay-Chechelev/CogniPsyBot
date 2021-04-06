
import telebot
import datetime
import threading
import sys, os
from db_works import Database
from CogniPsyBot import CogniPsyBot
from config import *

class Router:
    def __init__(self):
        self.token = TOKEN
        self.bot = telebot.TeleBot(self.token)  # класс бота с которым работаем
        self.database = Database()
        self.user = 0
        self.users_threads = []
        self.registered_users = []
        self.load_users()
        self.users_threads_done = False
        self.admin = 453297650

    def load_users(self):
        self.registered_users = self.database.get_user_list()
        print('Registred Users - ', self.registered_users)
        for i in self.registered_users:
            print("Startig user ", i)
            self.run_user(i)
        return True

    def run_user(self, user):
        try:
            self.users_threads.append(CogniPsyBot(self.bot, user))
            print("Thead for {} successfully started".format(user))
        except:
            print("Error! {}".format(user))
            pass

    def any_text(self):
        @self.bot.message_handler(content_types=['text'])
        def on_text(message):
            self.bot.send_message(self.admin, 'LOGGING ---------- ПОЛЬЗОВАТЕЛЬ {0} {1} {2} ОТПРАВИЛ (TEXT) {3}'.format(
                message.chat.id, message.chat.first_name, message.chat.last_name, message.text))
            if message.text == 'reboot' and message.chat.id == self.admin:
                os.system('reboot')
            if not(message.chat.id in self.registered_users):
                self.run_user(message.chat.id)
                self.registered_users.append(message.chat.id)
            for i in self.users_threads:
                i.text_analize(message)

    def cmd_start(self):
        @self.bot.message_handler(commands=['start'])
        def on_text(message):
            self.bot.send_message(self.admin, 'LOGGING ---------- ПОЛЬЗОВАТЕЛЬ {0} {1} {2} ОТПРАВИЛ (COMMAND) {3}'
                                              ''.format(message.chat.id, message.chat.first_name,
                                                        message.chat.last_name, message.text))
            if not(message.chat.id in self.registered_users):
                self.run_user(message.chat.id)
                self.registered_users.append(message.chat.id)
            for i in self.users_threads:
                i.start_command(message)

    def answer_handler(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            self.bot.send_message(self.admin, 'LOGGING ---------- ПОЛЬЗОВАТЕЛЬ {0} {1} {2} ОТПРАВИЛ (CALLBACK) {3}'
                                              ''.format(call.message.chat.id, call.message.chat.first_name,
                                                        call.message.chat.last_name, call.data))
            if not(call.message.chat.id in self.registered_users):
                self.run_user(call.message.chat.id)
                self.registered_users.append(call.message.chat.id)
            for i in self.users_threads:
                i.answer_handler(call)

    def main_start(self):
        self.bot.send_message(self.admin, 'ERROR ---------- ПРОИЗОШЛА ПЕРЕЗАГРУЗКА БОТА!!!')
        self.cmd_start()
        self.any_text()
        self.answer_handler()
        self.bot.polling()


done = False

while not done:
    print('START BOT >>>')
    bot = Router()
    try:
        bot.main_start()
        print('EXEPTION... RESTART >>>')
    except:
        print('EXEPTION... RESTART >>>')
        data = '\n\n\n\n{}------------------------------------\n'.format(datetime.datetime.now())
        data += str(sys.exc_info()[0])
        f = open(FILE_PATH + 'error-{}.log'.format(datetime.datetime.now()), 'w')
        f.write(data)
        f.close()
        print(data)






