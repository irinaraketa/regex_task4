import os
import json
import inspect
import re

DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = f"{DIR}/data/"


class User:
    def __init__(self, user_hash):
        self.user_name = user_hash["user_name"]
        self.user_password = user_hash["user_password"]

    @staticmethod
    def load_users():
        data = []
        if os.path.isfile(PATH_DATA + "users.json"):
            with open(PATH_DATA + "users.json", "r", encoding="utf-8") \
                      as read_file:
                data = json.load(read_file)
        return data

    def user_registration(user_name, user_password, users) -> bool:
        for user in users:
            if user['user_name'] == user_name:  # Такой пользователь уже зарегистрирован
                return False
        users.append({"user_name": user_name, \
                      "user_password": user_password})
        with open(PATH_DATA + "users.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)
        return True

    def user_authorization(user_name, user_password, users):
        for user in users:
            if user['user_name'] == user_name and \
               user['user_password'] == user_password:
                return True
        return False

    def is_user_exist(user_to_search, users) -> bool:
        for user in users:
            if user['user_name'] == user_to_search:
                return True
        return False

class Controller:

    @staticmethod
    def writing_data(user_name, text):
        name_and_tag = ', '.join(set(re.findall(r'(#\w+|@\w+)', text)))
        data = Controller.load_data()
        data = data + [{"user_name": user_name, \
                        "name_and_tag": name_and_tag, \
                        "text": text}]
        with open(PATH_DATA + "data.json", "w", encoding="utf-8") \
                  as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_data():
        data = []
        if os.path.isfile(PATH_DATA + "data.json"):
            with open(PATH_DATA + "data.json", "r", encoding="utf-8") \
                      as data_file:
                data = json.load(data_file)
        return data if data else []

    def print_found(what_look):
        data = Controller.load_data()
        for letter in data:
            if what_look in letter['name_and_tag'].lower():
                print(letter['text'])

while True:
    print(inspect.cleandoc('''Что желаете (введите номер пункта):
                        1. Зарегистрироваться
                        2. Авторизироваться
                        3. (или любой другой символ). Выйти из программы
                        '''))
    user_choice = input()
    if user_choice == '1':  # Регистрация
        user_name = input("Введите ваш ник: ")
        if len(user_name) == 0:
            print('Имя пользователя не может быть пустым')
            continue
        user_password = input('Введите ваш пароль: ')
        users = User.load_users()
        if User.user_registration(user_name, user_password, users):
            print('Пользователь успешно добавлен')
        else: 
            print('Ошибка регисрации пользователя')
        continue
    elif user_choice == '2':  # Авторизация
        user_name = input("Введите ваш ник: ")
        user_password = input('Введите ваш пароль: ')
        users = User.load_users()
        if not User.user_authorization(user_name, user_password, users):
            print('Ошибка в имени или пароле пользователя')
            continue
        else:
            break
    elif user_choice == '3':  # Выход из программы
        raise SystemExit
    else:
        print('Такого варианта не предусмотррено')
        continue
user = User({"user_name": user_name, "user_password": user_password})
print(inspect.cleandoc('''Что желаете (введите номер пункта):
                    1. Добавить текст
                    2. Поиск по хэштегу.
                    3. Поиск по имени пользователя в тексте.
                    4. Поиск по текстам конкретного пользователя.
                    '''))
user_choice = input()
if user_choice == '1':  # Добавить текст
    text = input('Введите ваш текст: ')
    Controller.writing_data(user_name, text)
elif user_choice == '2':  # Поиск по хэштегу
    tag_to_search = input('Введите хэштег: ').lower()
    if len(tag_to_search) < 3:
        print('Минимальная длина хештега для поиска 3')
        raise SystemExit
    while tag_to_search[-1] in 'уеёаоэяиюый':  # Убирем окончание
        tag_to_search = tag_to_search[:len(tag_to_search)-1]
    if tag_to_search.startswith('#'):
        Controller.print_found(tag_to_search)
    else:
        Controller.print_found('#' + tag_to_search)
elif user_choice == '3':  # Поиск по имени пользователя в тексте
    user_to_search = input('Введите иимя пользователя: ')
    if len(user_to_search) == 0:
        print('Имя пользователя не может быть пустым')
    else:
        if User.is_user_exist(user_to_search, users):
            Controller.print_found('@' + user_to_search)
elif user_choice == '4':  # Поиск по текстам конкретного пользователя
    user_to_search = input('Введите иимя пользователя: ')
    if len(user_to_search) == 0:
        print('Имя пользователя не может быть пустым')
    else:
        data = Controller.load_data()
        for letter in data:
            if user_to_search == letter['user_name']:
                print(letter['text'])
                
