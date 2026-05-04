from services.auth_service import register, login
from services.order_service import client_menu, restaurant_menu, courier_menu

def main():
    while True:
        print("\n=== СЕРВИС ДОСТАВКИ ЕДЫ ===")
        print("1. Регистрация")
        print("2. Вход")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                if user["role"] == "client":
                    client_menu(user)
                elif user["role"] == "restaurant":
                    restaurant_menu(user)
                elif user["role"] == "courier":
                    courier_menu(user)
        elif choice == "0":
            break

if __name__ == "__main__":
    main()