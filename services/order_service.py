from services.file_service import load_data, save_data

ORDERS_FILE = "data/orders.txt"

# ================= CLIENT =================

def client_menu(user):
    # Временная корзина клиента
    cart = []

    while True:
        print("\n=== КЛИЕНТ ===")
        print("1. Добавить в корзину")
        print("2. Оформить заказ")
        print("3. Мои заказы")
        print("0. Назад")

        choice = input("Выбор: ")

        if choice == "1":
            item = input("Введите блюдо: ")
            cart.append(item)
            print("Добавлено!")

        elif choice == "2":
            orders = load_data(ORDERS_FILE)
            # Формирование нового заказа
            order = {
                "id": len(orders) + 1,
                "client": user["username"],
                "items": cart,
                "status": "Создан"
            }

            orders.append(order)
            save_data(ORDERS_FILE, orders)

            cart.clear()
            print("Заказ оформлен!")

        elif choice == "3":
            orders = load_data(ORDERS_FILE)
            for o in orders:
                if o["client"] == user["username"]:
                    print(o)

        elif choice == "0":
            break


# ================= RESTAURANT =================
RESTAURANTS_FILE = "data/restaurants.txt"

def get_restaurant(username):
    restaurants = load_data(RESTAURANTS_FILE)

    for r in restaurants:
        if r["username"] == username:
            return r

    # Создание ресторана, если он отсутствует в системе
    new_restaurant = {
        "username": username,
        "menu": []
    }

    restaurants.append(new_restaurant)
    save_data(RESTAURANTS_FILE, restaurants)

    return new_restaurant


def save_restaurant(updated_restaurant):
    restaurants = load_data(RESTAURANTS_FILE)

    for i, r in enumerate(restaurants):
        if r["username"] == updated_restaurant["username"]:
            restaurants[i] = updated_restaurant

    save_data(RESTAURANTS_FILE, restaurants)

def show_restaurants():

    # Загрузка ресторанов из файла
    restaurants = load_data(RESTAURANTS_FILE)

    # Проверка наличия ресторанов
    if not restaurants:
        print("Ресторанов пока нет")
        return

    print("\n=== СПИСОК РЕСТОРАНОВ ===")

    # Вывод списка ресторанов
    for index, restaurant in enumerate(restaurants, start=1):
        print(f"{index}. {restaurant['username']}")

def restaurant_menu(user):

    # Получение данных ресторана
    restaurant = get_restaurant(user["username"])

    while True:
        print("\n=== РЕСТОРАН ===")
        print("1. Посмотреть меню")
        print("2. Добавить блюдо")
        print("3. Удалить блюдо")
        print("4. Посмотреть заказы")
        print("5. Изменить статус заказа")
        print("0. Назад")

        choice = input("Выбор: ")

        # ================= ПРОСМОТР МЕНЮ =================

        if choice == "1":

            if not restaurant["menu"]:
                print("Меню пустое")
            else:
                print("\n=== МЕНЮ ===")

                for index, item in enumerate(restaurant["menu"], start=1):
                    print(
                        f"{index}. "
                        f"{item['name']} | "
                        f"{item['category']} | "
                        f"{item['price']} руб."
                    )

        # ================= ДОБАВЛЕНИЕ БЛЮДА =================

        elif choice == "2":

            name = input("Название блюда: ")
            category = input("Категория: ")
            price = float(input("Цена: "))

            dish = {
                "name": name,
                "category": category,
                "price": price
            }

            # Добавление блюда в меню
            restaurant["menu"].append(dish)

            # Сохранение изменений
            save_restaurant(restaurant)

            print("Блюдо успешно добавлено!")

        # ================= УДАЛЕНИЕ БЛЮДА =================

        elif choice == "3":

            if not restaurant["menu"]:
                print("Меню пустое")
                continue

            print("\n=== МЕНЮ ===")

            for index, item in enumerate(restaurant["menu"], start=1):
                print(f"{index}. {item['name']}")

            dish_index = int(input("Введите номер блюда: ")) - 1

            if 0 <= dish_index < len(restaurant["menu"]):

                deleted_dish = restaurant["menu"].pop(dish_index)

                save_restaurant(restaurant)

                print(f"Блюдо '{deleted_dish['name']}' удалено!")

            else:
                print("Неверный номер блюда")

        # ================= ПРОСМОТР ЗАКАЗОВ =================

        elif choice == "4":

            orders = load_data(ORDERS_FILE)

            if not orders:
                print("Заказов пока нет")
            else:
                for order in orders:
                    print(order)

        # ================= ИЗМЕНЕНИЕ СТАТУСА =================

        elif choice == "5":

            orders = load_data(ORDERS_FILE)

            order_id = int(input("ID заказа: "))

            print("\nДоступные статусы:")
            print("1. Принят")
            print("2. Готовится")
            print("3. Готов к выдаче")

            status_choice = input("Выбор: ")

            statuses = {
                "1": "Принят",
                "2": "Готовится",
                "3": "Готов к выдаче"
            }

            if status_choice not in statuses:
                print("Неверный выбор")
                continue

            for order in orders:

                if order["id"] == order_id:

                    # Обновление статуса заказа
                    order["status"] = statuses[status_choice]

                    save_data(ORDERS_FILE, orders)

                    print("Статус успешно изменён!")
                    break

            else:
                print("Заказ не найден")

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню")


# ================= COURIER =================

def courier_menu(user):
    while True:
        print("\n=== КУРЬЕР ===")
        print("1. Доступные заказы")
        print("2. Взять заказ")
        print("3. Завершить заказ")
        print("0. Назад")

        choice = input("Выбор: ")
        orders = load_data(ORDERS_FILE)

        if choice == "1":
            for o in orders:
                if o["status"] == "Готов к выдаче":
                    print(o)

        elif choice == "2":
            order_id = int(input("ID заказа: "))
            for o in orders:
                if o["id"] == order_id:
                    # Курьер принимает заказ
                    o["status"] = "В пути"
                    o["courier"] = user["username"]

            save_data(ORDERS_FILE, orders)

        elif choice == "3":
            order_id = int(input("ID заказа: "))
            for o in orders:
                if o["id"] == order_id:
                    o["status"] = "Доставлен"

            save_data(ORDERS_FILE, orders)

        elif choice == "0":
            break