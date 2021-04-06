import telebot
import os
from db_works import Database
from datetime import timedelta
from tests.BeckTest import BeckTest
from tests.BeckRemasteredTest import BeckRemasteredTest
from tests.LihiTest1 import LihiTest1
from tests.LihiTest2 import LihiTest2
from tests.TaylorTest import TaylorTest
from tests.SelfishTest import SelfishTest
from tests.JersildTest import JersildTest
from tests.Introduction import Introduction
from games.Faces_game import FaceGame
from config import *
from timer import Timer
import threading


class CogniPsyBot:
    def __init__(self, bot, user):
        # переменные бота
        self.bot = bot
        self.database = Database()
        self.last_message_id = 0
        self.user = user
        self.timer = None
        self.timer_thread = None
        try:
            self.timer = Timer(self.bot, self.user)
            self.timer_thread = threading.Thread(target=self.timer.timer, args=(None,))
            self.timer_thread.start()
        except:
            pass
        self.admin = 453297650
        self.intro_photos = os.listdir(FILE_PATH + 'images/introduction')
        for i in self.intro_photos:
            if not 'png' in i:
                del self.intro_photos[self.intro_photos.index(i)]
        self.intro_photos.sort()

        # переменные теста
        self.test = None  # класс теста, который будет подгружаться в процессе
        self.question = 0  # счетчик вопросов в тесте
        self.test_mode = False

        # переменные дневника
        self.dairy_mode = False  # флаг режима дневника
        self.dairy = ''  # класс двевника , который будет подгружаться в процессе
        self.history = []  # история записей (даты)

        # переменные игры
        self.game_mode = False
        self.game = None
        self.test_n_game_answer = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

        self.feedback_mode = False

        # Клавиатура настроения
        import keyboards.MorningKB as MorningKB
        self.MorningKB = MorningKB.layout()

        # Основная клавиатура пользователя
        import keyboards.MainUserMenu as MainMenu
        self.TestDiaryKB = MainMenu.layout()

        # клавиатура Дневника (кнопка завершить)
        import keyboards.DiaryKB as DiaryKB
        self.FinishKB = DiaryKB.layout()

        # клавиатура Тестов
        import keyboards.TestKB as TestKB
        self.TestKB = TestKB.layout()

        # клавиатура меню игр
        import keyboards.GamesKB as GamesKB
        self.GamesKB = GamesKB.layout()

        # Клавиатура психообразования
        import keyboards.EducationKB as EducationKB
        self.EduKB = EducationKB.layout()

        # Клавиатура HELP
        import keyboards.HelpKB as HelpKB
        self.HelpKB = HelpKB.layout()

        # база пользователей
        self.registered_users = []
        self.registration_mode = False
        self.psycho_id = 0
        self.psycho_id_state = False
        self.e_mail = ''
        self.e_mail_state = False
        self.sex = ''
        self.date_of_birth = ''
        self.year = '1990'
        self.month = '1'
        self.day = '1'
        self.year_state = False
        self.month_state = False
        self.day_state = False
        self.password = ''
        self.password_state = False
        self.load_users()
        pass

    def load_users(self):
        self.registered_users = self.database.get_user_list()
        return True

    def register_new_user(self, message, psycho_id, e_mail, sex, date_of_birth, password, utc):
        try:
            self.database.register_new_user(message, psycho_id, e_mail, sex, date_of_birth, password, utc)
            self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ РЕГИСТРАЦИЯ {0} {1} {2}'.format(
                message.chat.id, message.chat.first_name, message.chat.last_name))
        except:
            self.bot.send_message(self.admin, 'LOGGING ---------- ОШИБКА РЕГИСТРАЦИИ {0} {1} {2}'.format(
                message.chat.id, message.chat.first_name, message.chat.last_name))
        self.registration_mode = False
        return True

    def start_registration(self, message):
        self.registration_mode = True
        self.registered_users.append(message.chat.id)
        self.test = Introduction(self.bot, message)
        text, button = self.test.get_question()
        self.bot.send_message(message.chat.id,
                              text,
                              reply_markup=button)
        self.question = self.test.number_of_question
        return True

    def show_main_menu(self, message):
        self.test = None
        self.test_mode = False
        self.dairy_mode = False
        self.game_mode = False
        self.registration_mode = False
        self.bot.send_message(message.chat.id,
                              "Добро пожаловать, {}, в твою комнату. Здесь ты можешь расслабиться "
                              "и быть уверенными что тебя никто не упрекнет и всегда поддержат.\n"
                              "Я помогу тебе вести дневник, проведу некоторые тесты и иногда буду "
                              "предлагать поиграть в игры.\n Так же несколько раз в день я буду присылвть тебе "
                              "интересные статьи и топики, ну и, естественно, задания.".format(message.chat.first_name),
                              reply_markup=self.TestDiaryKB)
        return True

    def start_command(self, message):
        if not message.chat.id == self.user:
            return True
        if message.chat.id in self.registered_users:
            self.show_main_menu(message)
            return True
        else:
            self.start_registration(message)
            return True

    def text_analize(self, message):
        if not message.chat.id == self.user:
            return True
        if not message.chat.id in self.registered_users:
            self.start_registration(message)
            return True

        rmKB = telebot.types.ReplyKeyboardRemove()
        # self.check_registration(message)
        if self.dairy_mode:  # если включен режим дневника
            if message.text == 'Завершить':
                print(message.text)
                self.dairy_mode = False
                if self.dairy != '':
                    self.bot.send_message(message.chat.id,
                                          "Новая запись в дневник:\n\n" + self.dairy,
                                          reply_markup=rmKB)
                    try:
                        self.database.simple_diary_record(message, self.dairy)
                        self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ ДНЕВНИКА {0} {1} {2}'.format(
                            message.chat.id, message.chat.first_name, message.chat.last_name))
                    except:
                        self.bot.send_message(self.admin,
                                              'ERROR ---------- ОШИБКА ЗАПИСИ ДНЕВНИКА {0} {1} {2}'.format(
                                                  message.chat.id, message.chat.first_name, message.chat.last_name))
                else:
                    self.bot.send_message(message.chat.id,
                                          "Запись пустая.",
                                          reply_markup=rmKB)
                self.dairy = ''
                self.bot.send_message(message.chat.id,
                                      "Выбери действие:",
                                      reply_markup=self.TestDiaryKB)
                return True
            self.dairy += message.text + '\n'  # в переменнцю записываем все сообщения до нажатия кнопки конец
        if message.text == 'Завершить':
            self.test = None
            self.test_mode = False
            self.dairy_mode = False
            self.game_mode = False
            try:
                self.bot.delete_message(message.chat.id, message.message_id - 2)
            except:
                pass
            try:
                self.bot.delete_message(message.chat.id, message.message_id - 1)
            except:
                pass
            self.bot.delete_message(message.chat.id, message.message_id)
            self.bot.send_message(message.chat.id,
                                  "Главное меню...",
                                  reply_markup=rmKB)
            self.bot.send_message(message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True
        if self.feedback_mode:
            self.bot.send_message(self.admin,
                                  "НОВОЕ СООБЩЕНИЕ С ОТЗЫВОМ ОТ ПОЛЬЗОВАТЕЛЯ {}\n\n".format(message.chat.id) +
                                  message.text,
                                  reply_markup=rmKB)
            self.bot.send_message(message.chat.id,
                                  "Отзыв успешно отправлен! Спасибо!",
                                  reply_markup=rmKB)
            self.bot.send_message(message.chat.id,
                                  "Выбери действие...",
                                  reply_markup=self.TestDiaryKB)
            self.feedback_mode = False
            return True

    def answer_handler(self, call):
        if not call.message.chat.id == self.user:
            return True
        if not (call.message.chat.id in self.registered_users):
            self.start_registration(call.message)
            return True
        endKB = telebot.types.ReplyKeyboardMarkup()
        endKB.row('Завершить')
        choice = call.data
        if choice == 'next' and self.registration_mode:
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            text, button = self.test.get_question()
            if 4 <= self.question <= 11:
                f = open(FILE_PATH + 'images/introduction/' + self.intro_photos[self.question - 4], 'rb')
                self.bot.send_photo(call.message.chat.id, f, caption=str(text), reply_markup=button)  #
                f.close()
            else:
                self.bot.send_message(call.message.chat.id,
                                      text,
                                      reply_markup=button)
            self.question = self.test.number_of_question
            return True
        if choice in ['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ] and self.registration_mode:
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            utc = timedelta(hours=int(choice) + 3)
            self.register_new_user(call.message, 'NONE', 'NONE', 'NONE', '1900-01-01', 'NONE', utc)
            self.timer = Timer(self.bot, self.user)

            self.test = None
            self.test_mode = True
            self.test = BeckRemasteredTest(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Перед тобой тест (21 вопрос) на уровень депрессии Аарона Беке (создателя "
                                  "когнитивно-поведенческой тепрапии CBT). Благодаря данному тесту, мы сможем "
                                  "определить, есть ли у тебя депрессия и насколько сильно она имеет место быть в "
                                  "твоей жизни. Тебе необходимо выбрать один ответ, который, как можно ближе "
                                  "отражает твое настоящее состояние. Так же хочу напомнить, что результаты "
                                  "данного теста, не являются постановкой диагноза, а помогают лишь определить "
                                  "направление работы. Мы всегда рекомендуем обращаться к врачу.")
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        # ******************   ТЕСТЫ  *****************************************
        if choice == 'test':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Выбери интересующий тест для прохождения.",
                                  reply_markup=self.TestKB)
            return True

        if choice == 'beck':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = BeckTest(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Выбери соответствующее твоему состоянию утверждение, нажав соответству"
                                  "ющую кнопку. Всего 21 вопрос.",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        if choice == 'anxiety':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = LihiTest1(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Оцени насколько типично для тебя поведение, описанное в каждом из утверждений.",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        if choice == 'lifeanxiety':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = LihiTest2(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Укажи насколько сильно ты обеспокоен. Нажми соответствующую кнопку.",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        if choice == 'taylor':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = TaylorTest(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Опросник предложен J.Teylor и предназначен для измерения уровня тревожности. "
                                  "Адаптирован Немчиным Т.А. Опросник состоит из 50 утверждений, на которые "
                                  "следует дать ответ \"да\" или\"нет\".",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        if choice == 'selfish':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = SelfishTest(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Тест на самооценку (33 вопроса) определит уровень твоего самоуважения и любви к "
                                  "себе.",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True

        if choice == 'jersild':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test_mode = True
            self.test = JersildTest(self.bot, call.message)
            self.bot.send_message(call.message.chat.id,
                                  "Опросник Психические состояния личности Джерсайлда (Arthur Thomas Jersild). "
                                  "Направлен на выявление таких стойких негативных внутренних состояний, "
                                  "как одиночество, ощущение бессмысленность существования, половой конфликт, "
                                  "враждебный настрой, безнадежность и др.",
                                  reply_markup=endKB)
            self.test.get_question()
            self.question = self.test.number_of_question
            return True
        # ******************   ЗАДАНИЯ  *****************************************
        if choice == 'tasks':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Прости, но данное меню сейчас находится в разработке. Я напишу тебе как только меня "
                                  "обновят!",
                                  reply_markup=endKB)
            return True
        # ******************   УПРАЖНЕНИЯ  *****************************************
        if choice == 'exercises':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Прости, но данное меню сейчас находится в разработке. Я напишу тебе как только меня "
                                  "обновят!",
                                  reply_markup=endKB)
            return True
        # ******************   ДНЕВНИК  *****************************************
        logKB = telebot.types.InlineKeyboardMarkup()
        if choice == 'diary':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.dairy_mode = True
            self.dairy = ''
            self.bot.send_message(call.message.chat.id,
                                  "Это твой дневник!\nЗдесь ты можешь писать все свои мысли, истории, "
                                  "тревоги. Текст можно вводить несколькими сообщениями. Если ты решишь"
                                  " закончить запись - нажми кнопку Завершить.",
                                  reply_markup=self.FinishKB)
            self.history = self.database.show_dairy_logs(call.message.chat.id)
            if len(self.history) == 0:
                add = '\nУ тебя пока нет записей'
            else:
                add = ''
            for i in self.history:
                logKB.row(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
            self.bot.send_message(call.message.chat.id,
                                  "А так же ты можешь посмотреть историю твоих записей: " + add,
                                  reply_markup=logKB)
            return True

        if self.dairy_mode and choice in self.history:
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            record = self.database.show_current_record(call.message.chat.id, choice)
            for i in self.history:
                logKB.row(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
            self.bot.send_message(call.message.chat.id,
                                  "{} ты писал: \n".format(choice) + record + "\nМожешь выбрать другую дату или "
                                                                              "продолжить ввод.",
                                  reply_markup=logKB)
            return True

        # ******************   ОТВЕТЫ НА ИГРЫ И ТЕСТЫ  *****************************************
        if choice in self.test_n_game_answer:
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            if self.test_mode:
                self.test.result(int(choice))
                self.test.get_question()
                self.question = self.test.number_of_question
                if self.question == len(self.test.question):
                    self.test = None
                    self.test_mode = False
                    self.bot.send_message(call.message.chat.id,
                                          'Я запишу результаты в архив, чтоб я мог все проанализировать.\n'
                                          'Как у тебя настроение?',
                                          reply_markup=self.MorningKB)
                    if self.registration_mode:
                        self.timer_thread = threading.Thread(target=self.timer.timer, args=(None,))
                        self.timer_thread.start()
                        self.registration_mode = False

                return True
            if self.game_mode:
                if self.game.result(choice):
                    pass
                else:
                    self.game = None
                    self.game_mode = False
                    self.bot.send_message(call.message.chat.id,
                                          'Понравилось? Мы постараемся сделать по-больше интересных игр для тебя!\n'
                                          'Как у тебя настроение?',
                                          reply_markup=self.MorningKB)
                return True

        # ******************  МЕНЮ НАСТРОЕНИЯ *****************************************
        if choice == 'exhausted_mood':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                self.database.mood_result(call.message.chat.id, choice)
                self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            except:
                self.bot.send_message(self.admin, 'ERROR ---------- ОШИБКА ЗАПИСИ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True
        if choice == 'bad_mood':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                self.database.mood_result(call.message.chat.id, choice)
                self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            except:
                self.bot.send_message(self.admin, 'ERROR ---------- ОШИБКА ЗАПИСИ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True
        if choice == 'normal_mood':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                self.database.mood_result(call.message.chat.id, choice)
                self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            except:
                self.bot.send_message(self.admin, 'ERROR ---------- ОШИБКА ЗАПИСИ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True
        if choice == 'good_mood':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                self.database.mood_result(call.message.chat.id, choice)
                self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            except:
                self.bot.send_message(self.admin, 'ERROR ---------- ОШИБКА ЗАПИСИ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True
        if choice == 'wonderful_mood':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            try:
                self.database.mood_result(call.message.chat.id, choice)
                self.bot.send_message(self.admin, 'LOGGING ---------- УСПЕШНАЯ ЗАПИСЬ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            except:
                self.bot.send_message(self.admin, 'ERROR ---------- ОШИБКА ЗАПИСИ НАСТРОЕНИЯ {0} {1} {2}'.format(
                    call.message.chat.id, call.message.chat.first_name, call.message.chat.last_name))
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True

        # ******************  ГЛАВНОЕ МЕНЮ  *****************************************
        if choice == 'mainmenu':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.test = None
            self.test_mode = False
            self.bot.send_message(call.message.chat.id,
                                  "Выбери действие:",
                                  reply_markup=self.TestDiaryKB)
            return True

        # ******************    ИГРЫ  *****************************************
        if choice == 'games':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Выбери игру:",
                                  reply_markup=self.GamesKB)
            return True

        if choice == 'faces':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.game_mode = True
            self.game = FaceGame(self.bot, call.message.chat.id)
            self.bot.send_message(call.message.chat.id,
                                  "На фотографии найде лицо с улыбкой и нажми соответствующую кнопку",
                                  reply_markup=endKB)
            self.game.start()
            return True
        # ******************   ПСИХООБРАЗОВАНИЕ  *****************************************
        if choice == 'education':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Я всегда стараеюсь подобрать самые актуальные статьи для саморазвития. Здесь "
                                  "ты можете ознакомиться со всеми полезными материалами, которые я подобрал для твоего"
                                  " курса.",
                                  reply_markup=self.EduKB)
            return True

        if choice == 'cog_dist':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            f = open(FILE_PATH + 'texts/Cognitive_Distortions.txt', 'r')
            text = f.read()
            f.close()
            self.bot.send_message(call.message.chat.id,
                                  text,
                                  reply_markup=self.EduKB)
            return True
        if choice == 'mod_abc':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            f = open(FILE_PATH + 'texts/ABC_model.txt', 'r')
            text = f.read()
            f.close()
            self.bot.send_message(call.message.chat.id,
                                  text,
                                  reply_markup=self.EduKB)
            return True
        # ******************   ОБРАТНАЯ СВЯЗЬ  *****************************************
        if choice == 'feedback':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.feedback_mode = True
            self.bot.send_message(call.message.chat.id,
                                  "Спасибо, что решил оставить отзыв обо мне сервисе! Я стремлюсь быть лучше и мои "
                                  "друзья мне в этом помогают. Напиши мне свои пожелания в ответ на это сообщение, "
                                  "и мы обязательно их учтем!",
                                  reply_markup=endKB)
            return True
        # ******************   РАЗДЕЛ ПОМОЩЬ  *****************************************
        if choice == 'help':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id,
                                  "Выбери интересующий пункт:",
                                  reply_markup=self.HelpKB)
            return True
        if choice == 'help_about':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            f = open(FILE_PATH + 'texts/help_about.txt', 'r')
            text = f.read()
            f.close()
            self.bot.send_message(call.message.chat.id,
                                  text,
                                  reply_markup=self.HelpKB)
            return True
        if choice == 'help_structure':
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            f = open(FILE_PATH + 'texts/help_structure.txt', 'r')
            text = f.read()
            f.close()
            self.bot.send_message(call.message.chat.id,
                                  text,
                                  reply_markup=self.HelpKB)
            return True
        return True
