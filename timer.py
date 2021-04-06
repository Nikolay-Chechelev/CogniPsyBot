from db_works import Database
from datetime import datetime
from datetime import timedelta
from therapy.standart_therapy import *
from time import sleep
from telebot import types

class Timer:
    def __init__(self, bot, user):
        self.user = user
        self.bot = bot
        self.database = Database()
        self.utc = self.database.get_user_utc(self.user)
        import keyboards.MorningKB as MorningKB
        self.MorningKB = MorningKB.layout()
        self.admin = 453297650
        self.bot.send_message(self.admin, 'ERROR ---------- ПРОИЗОШЕЛ ЗАПУСК НОВОГО ПОТОКА {}'.format(self.user))


    def get_users_time(self):
        time = timedelta(hours=datetime.now().hour) + self.utc
        print(time)
        return time

    def say_good_morning(self):
        self.bot.send_message(self.user,
                              'Доброе утро! Искренне желаю тебе хорошего дня!\n'
                              'Как у тебя сегодня настроение?',
                              reply_markup=self.MorningKB)

    def suggest_face_game(self):
        self.bot.send_message(self.user,
                              'Надеюсь, у тебя все хорошо! Не хочешь поднять настроение, немного '
                              'поиграв?',
                              reply_markup=types.InlineKeyboardMarkup().row(
                                  types.InlineKeyboardButton(text='Игра Лица (повышает настроение)',
                                                             callback_data='faces')))

    def suggest_dairy(self):
        self.bot.send_message(self.user,
                              'Я уверен, что у тебя был насыщенный день! Не хочешь поделиться новостями'
                              ' или эмоциями?',
                              reply_markup=types.InlineKeyboardMarkup().row(
                                  types.InlineKeyboardButton(text='Дневник',
                                                             callback_data='diary')))

    def suggest_3_columns(self):
        self.bot.send_message(self.user,
                              'Давай сейчас запишем и проанализируем твои негативные мысли за сегодня? '
                              'Для лучшего реультата это нужно делать регулярно!',
                              reply_markup=types.InlineKeyboardMarkup().row(
                                  types.InlineKeyboardButton(text='Дневник 3 колонки',
                                                             callback_data='3_columns')))

    def say_goodnight(self):
        import keyboards.MainUserMenu as MainMenu
        self.bot.send_message(self.user,
                              'Спокойной ночи! Я надеюсь что завтра нас с тобой ждет пректрасный день!',
                              reply_markup=MainMenu.layout())

    def timer(self, *args):
        while 1:
            time = self.get_users_time()
            if True: ## therapy == standart_therapy

                for i in STANDART_THERAPY['therapy_list'].keys():
                    if i == 'mood':
                        for j in STANDART_THERAPY['therapy_list'][i]:
                            if time == j:
                                self.say_good_morning()
                    if i == 'face_game':
                        for j in STANDART_THERAPY['therapy_list'][i]:
                            if time == j:
                                self.suggest_face_game()
                    if i == 'dairy':
                        for j in STANDART_THERAPY['therapy_list'][i]:
                            if time == j:
                                self.suggest_dairy()
                    if i == 'columns':
                        for j in STANDART_THERAPY['therapy_list'][i]:
                            if time == j:
                                self.suggest_3_columns()
                    if i == 'goodnight':
                        for j in STANDART_THERAPY['therapy_list'][i]:
                            if time == j:
                                self.say_goodnight()
            #Пауза!
            sleep(3600)





# t = Timer(1, 453297650)
# print(t.get_users_time())
#for i in STANDART_THERAPY['therapy_list'].keys():
#    print(i, type(i), STANDART_THERAPY['therapy_list'][i])