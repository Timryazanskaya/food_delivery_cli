from services.file_service import load_data, save_data

USERS_FILE = "data/users.txt"

def register():
    users = load_data(USERS_FILE)

    username = input("Логин: ")
    password = input("Пароль: ")
    role = input("Роль (client/restaurant/courier): ")

    user = {
        "username": username,
        "password": password,
        "role": role
    }

    users.append(user)
    save_data(USERS_FILE, users)

    print("Регистрация успешна!")

def login():
    users = load_data(USERS_FILE)

    username = input("Логин: ")
    password = input("Пароль: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Успешный вход!")
            return user

    print("Ошибка входа")
    return None