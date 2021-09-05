import os
import json
import inspect
import re

DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = f"{DIR}/data/"


class UsernameEmptyError(Exception):
    def __init__(self):
        self.text = f"Ваш логин пустой"

    def __str__(self):
        return self.text

class UsernameNotCorrectError(Exception):
    def __init__(self, username):
        self.text = f"{username} должен начинаться с @"

    def __str__(self):
        return self.text

class UserAuthorizationError(Exception):
    def __init__(self):
        self.text = f"Ошибка в имени или пароле пользователя"

    def __str__(self):
        return self.text

class TagLenError(Exception):
    def __init__(self):
        self.text = f"Минимальная длина хештега 3"

    def __str__(self):
        return self.text

class User:
    @staticmethod
    def user_registration(user_name: str, user_password: str) -> str:
        users = read_json("users.json")
        if User.is_user_exist(user_name, users):
            return 'Такой пользователь уже существует'
        user = User({"user_name": user_name, \
                "user_password": user_password})
        user.__save_user_to_json(users)
        return 'Пользователь успешно зарегистрирован'

    @staticmethod
    def is_user_exist(user_to_search: str, users: list) -> bool:
        for user in users:
            if user['user_name'] == user_to_search:
                return True
        return False

    @staticmethod
    def is_user_name_correct(user_name: str) -> bool:
        if not len(user_name): raise UsernameEmptyError
        if not re.match(r"@\b\w+\b", user_name): 
            raise UsernameNotCorrectError(user_name)
        return True

    @staticmethod
    def user_authorization(user_name: str, user_password: str) -> bool:
        users = read_json("users.json")
        for user in users:
            if user['user_name'] == user_name and \
               user['user_password'] == user_password:
                return True
        raise UserAuthorizationError
        return False

    def __init__(self, user_hash):
        self.user_name = user_hash["user_name"]
        self.user_password = user_hash["user_password"]

    def __save_user_to_json(self, users: list):
        users.append({"user_name": user_name, \
                "user_password": user_password})
        with open(PATH_DATA + "users.json", "w", encoding="utf-8") \
                  as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)

class Controller:
    @staticmethod
    def writing_data(user_name: str, text: str):
        name_and_tag = ', '.join(set(re.findall(r'(#\w+|@\w+)', text)))
        data = read_json("data.json") + [{"user_name": user_name, \
                            "name_and_tag": name_and_tag, \
                                          "text": text}]
        with open(PATH_DATA + "data.json", "w", encoding="utf-8") \
                  as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)

    @staticmethod
    def search_tag(tag_to_search: str):
    # Поиск по хэштегу        
        if len(tag_to_search) < 3:
            raise TagLenError
        while tag_to_search[-1] in 'уеёаоэяиюый':  # Убирем окончание
            tag_to_search = tag_to_search[:len(tag_to_search)-1]
        if tag_to_search.startswith('#'):
            Controller.print_found(tag_to_search)
        else:
            Controller.print_found('#' + tag_to_search)

    @staticmethod
    def search_user(user_to_search: str):
    # Поиск по имени пользователя в тексте        
        if user.is_user_name_correct(user_to_search):
            users = read_json("users.json")
            if User.is_user_exist(user_to_search, users):
                Controller.print_found(user_to_search)

    @staticmethod
    def search_user_text(user_to_search: str):
    # Поиск по текстам конкретного пользователя        
        if user.is_user_name_correct(user_to_search):
            data = read_json("data.json")
            for letter in data:
                if user_to_search == letter['user_name']:
                    print(letter['text'])

    @staticmethod
    def print_found(what_look: str):
        for letter in read_json("data.json"):
            if what_look in letter['name_and_tag'].lower():
                print(letter['text'])

def read_json(file_name: str) -> list:
    if os.path.isfile(PATH_DATA + file_name):
        with open(PATH_DATA + file_name, "r", encoding="utf-8") \
                    as read_file:
            return json.load(read_file)
    return []

if __name__ == '__main__':
    while True:
        print(inspect.cleandoc('''Что желаете (введите номер пункта):
                            1. Зарегистрироваться
                            2. Авторизироваться
                            3. Выйти из программы
                            '''))
        user_choice = input()
        if user_choice == '1':  # Регистрация
            user_name = input("Введите ваш логин: ")
            user_password = input('Введите ваш пароль: ')
            try:
                user_correct = User.is_user_name_correct(user_name)
            except UsernameEmptyError:
                print("Ваш username пуст :(")
            except UsernameNotCorrectError:
                print("Ваш username введён неверно. Он должен начинаться @")
            else:
                if user_correct: print(User.user_registration(user_name, user_password))
            continue
        elif user_choice == '2':  # Авторизация
            user_name = input("Введите ваш ник: ")
            user_password = input('Введите ваш пароль: ')
            try:
                user_correct = User.user_authorization(user_name, user_password)
            except UserAuthorizationError:
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
        Controller.search_tag(tag_to_search)
    elif user_choice == '3':  # Поиск по имени пользователя в тексте
        user_to_search = input('Введите имя пользователя: ')
        Controller.search_user(user_to_search)
    elif user_choice == '4':  # Поиск по текстам конкретного пользователя
        user_to_search = input('Введите иимя пользователя: ')
        Controller.search_user_text(user_to_search)
