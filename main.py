import os
import json
import inspect

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

    @staticmethod
    def load_data():
        if os.path.isfile(PATH_DATA + "data.json"):
            with open(PATH_DATA + "data.json", "r", encoding="utf-8") \
                      as data_file:
                data = json.load(data_file)
        else:
            data = []
        return data

    @staticmethod
    def writing_data(user_name, text):
        data = user.load_data()
        data = data + [{"user_name": user_name, \
                        "text": text}]
        with open(PATH_DATA + "data.json", "w", encoding="utf-8") \
                  as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)

    def user_registration(user_name, user_password, users):
        for user in users:
            if user['user_name'] == user_name:
                return 'Такой пользователь уже зарегистрирован'
        users.append({"user_name": user_name, \
                      "user_password": user_password})
        with open(PATH_DATA + "users.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)
        return 'Пользователь успешно добавлен'

    def user_authorization(user_name, user_password, users):
        for user in users:
            if user['user_name'] == user_name and \
               user['user_password'] == user_password:
                return True
        return False

    def is_user_exist(user_to_search, users):
        for user in users:
            if user['user_name'] == user_to_search:
                return True
        return False

    def print_found(what_look):
        data = user.load_data()
        for letter in data:
            if what_look in letter['text'].lower():
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
        user_password = input('Введите ваш пароль: ')
        users = User.load_users()
        print(User.user_registration(user_name, user_password, users))
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
    user.writing_data(user_name, text)
elif user_choice == '2':  # Поиск по хэштегу.
    tag_to_search = input('Введите хэштег: ')
    User.print_found(tag_to_search.lower())
elif user_choice == '3':  # Поиск по имени пользователя в тексте
    user_to_search = input('Введите иимя пользователя: ')
    if User.is_user_exist(user_to_search, users):
        User.print_found('@' + user_to_search)
elif user_choice == '4':  # Поиск по текстам конкретного пользователя
    user_to_search = input('Введите иимя пользователя: ')
    data = user.load_data()
    for letter in data:
        if user_to_search == letter['user_name']:
            print(letter['text'])
