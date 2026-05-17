from services.file_service import load_data, save_data

USERS_FILE = "data/users.txt"

def register():
    users = load_data(USERS_FILE)

    username = input("Логин: ")
    # Проверка существования пользователя
    for user in users:
        if user["username"] == username:
            print("Пользователь уже существует")
            return

    password = input("Пароль: ")
    role = input("Роль (client/restaurant/courier): ")

    user = {
        "username": username,
        "password": password,
        "role": role
    }
    # Добавление нового пользователя в список
    users.append(user)
    save_data(USERS_FILE, users)

    print("Регистрация успешна!")

def login():
    users = load_data("data/users.txt")

    username = input("Логин: ")
    password = input("Пароль: ")

    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                print(f"Успешный вход! Добро пожаловать, {username}!")
                return user
            else:
                print("Неверный пароль")
                return None

    print("Пользователь не найден")
    return None