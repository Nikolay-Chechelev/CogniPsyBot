import pymysql
import datetime
from config import *

class Database:
    def __init__(self):
        self.db_host = DB_HOST# '127.0.0.1'
        self.db_user = DB_USER# 'root'
        self.db_password = DB_PASSWORD#'4196567Aa'/'5uu5wuwub'
        self.db_name = DB_NAME
        self.database = pymysql.connect(self.db_host, self.db_user, self.db_password, self.db_name)
        self.cursor = self.database.cursor()

    def get_user_list(self):
        list = []
        self.cursor.execute("select * from user_data_db")
        ver = self.cursor.fetchall()
        for i in range(len(ver)):
            list.append(int(ver[i][0]))
        return list

    def register_new_user(self, message, psycho_id, e_mail, sex, date_of_birth, password, utc):
        chat_id = message.chat.id
        first_name = message.chat.first_name
        last_name = message.chat.last_name
        # chat_id = 1
        # first_name = "лолотлот"
        # last_name = "шгасгрщог"
        registration_date = datetime.datetime.now()
        self.cursor.execute(
            "insert into user_data_db "
            "(chat_id, first_name, last_name, psychologist_id, registration_date, e_mail, sex, date_of_birth, password, utc) "
            "values ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(
                chat_id, first_name, last_name, psycho_id, registration_date, e_mail, sex, date_of_birth, password, utc
            ))
        self.database.commit()
        return True

    def get_user_utc(self, user):
        self.cursor.execute(
            "select utc from user_data_db where chat_id={}".format(user))
        answer = self.cursor.fetchall()[0][0]
        return answer

    def diary_3_colomns_record(self, message, irrat_belifs, cog_dist, rat_belifs):
        chat_id = message.chat.id
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into 3_colomns_db "
            "(chat_id, record_date, irrational_belifs, cognitive_distortions, rational_belifs) "
            "values ({0}, '{1}', '{2}', '{3}', '{4}')".format(
                chat_id, record_datetime, irrat_belifs, cog_dist, rat_belifs
            ))
        self.database.commit()
        return True

    def simple_diary_record(self, message, text):
        chat_id = message.chat.id
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into diary_db "
            "(chat_id, record_date, thoughts_diary) "
            "values ({0}, '{1}', '{2}')".format(
                chat_id, record_datetime, text
            ))
        self.database.commit()
        return True

    def show_dairy_logs(self, user):
        self.cursor.execute(
            "select record_date from diary_db where chat_id={}".format(user))
        answer = self.cursor.fetchall()
        dates = []
        for i in answer:
            dates.append(str(i[0]))
        return dates

    def show_current_record(self, user, date):
        self.cursor.execute(
            "select thoughts_diary from diary_db where chat_id={0} and record_date='{1}'".format(user, date))
        answer = self.cursor.fetchall()
        return answer[0][0]

    def beck_test_result(self, user, text, result, cog, somat):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into beck_test_db "
            "(chat_id, test_date, test_result, points, cognitive_affective, somatic_appearing) "
            "values ({0}, '{1}', '{2}', {3}, {4}, {5})".format(
                user, record_datetime, text, result, cog, somat))
        self.database.commit()

    def jersild_test_result(self, user, text, d1, d2, d3, d4, d5, d6, d7, d8, d9):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into jersild_test_db "
            "(chat_id, test_date, test_result, loneliness, meaninglessness_of_existence, freedom_of_choise, "
            "gender_conflict, hostile_conflict, real_n_ideal_differ, free_will, hopelessness, feeling_of_homelessness) "
            "values ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11})".format(
                user, record_datetime, text, d1, d2, d3, d4, d5, d6, d7, d8, d9))
        self.database.commit()

    def lihi_test_1_result(self, user, text, result):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into lihi_test_1_db "
            "(chat_id, test_date, test_result, points) "
            "values ({0}, '{1}', '{2}', {3})".format(
                user, record_datetime, text, result))
        self.database.commit()

    def lihi_test_2_result(self, user, text, d1, d2, d3, d4, d5, d6):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into lihi_test_2_db "
            "(chat_id, test_date, test_result, people_relations_problems, trust_problems, future_meaninglessness, "
            "work_problems, financial_problems, all_points) "
            "values ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8})".format(
                user, record_datetime, text, d1, d2, d3, d4, d5, d6))
        self.database.commit()

    def selfish_test_result(self, user, text, result):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into selfish_test_db "
            "(chat_id, test_date, test_result, points) "
            "values ({0}, '{1}', '{2}', {3})".format(
                user, record_datetime, text, result))
        self.database.commit()

    def taylor_test_result(self, user, text, result):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into taylor_test_db "
            "(chat_id, test_date, test_result, points) "
            "values ({0}, '{1}', '{2}', {3})".format(
                user, record_datetime, text, result))
        self.database.commit()

    def logger(self, user, act_type, from_who, data, json, program_logs):
        log_date = datetime.datetime.now()
        print(
            "insert into logger_db "
            "(date, chat_id, act_type, act_from, act_data, act_json, error_logs) "
            "values (\"{0}\", {1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\")".format(
                log_date, user, act_type, from_who, data, json, program_logs))
        self.cursor.execute(
            "insert into logger_db "
            "(date, chat_id, act_type, act_from, act_data, act_json, error_logs) "
            "values (\"{0}\", {1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\")".format(
                log_date, user, act_type, from_who, data, json, program_logs))
        self.database.commit()

    def mood_result(self, user, mood):
        record_datetime = datetime.datetime.now()
        self.cursor.execute(
            "insert into mood_db "
            "(date, user_id, mood) "
            "values ('{0}', {1}, '{2}')".format(
                record_datetime, user, mood))
        self.database.commit()



# d = Database()
# a = d.mood_therapy_record_check(datetime.datetime.now(), 453297650)
# print(a)