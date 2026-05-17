from services.file_service import load_data, save_data

ORDERS_FILE = "data/orders.txt"

# ================= CLIENT =================

def client_menu(user):
    # Временная корзина клиента
    cart = []

    while True:
        print("\n=== КЛИЕНТ ===")
        print("1. Посмотреть рестораны")
        print("2. Посмотреть меню ресторана")
        print("3. Добавить в корзину")
        print("4. Посмотреть корзину")
        print("5. Оформить заказ")
        print("6. Мои заказы")
        print("0. Назад")

        choice = input("Выбор: ")

        if choice == "1":
            show_restaurants()

        elif choice == "2":
            show_restaurant_menu()


        elif choice == "3":
            add_to_cart(cart)

        elif choice == "4":
            show_cart(cart)

        elif choice == "5":
            orders = load_data(ORDERS_FILE)
            # Подсчёт суммы заказа
            total_price = sum(item["price"] for item in cart)
            # Формирование нового заказа
            order = {
                "id": len(orders) + 1,
                "client": user["username"],
                "items": cart,
                "total_price": total_price,
                "status": "Создан"
            }

            orders.append(order)
            save_data(ORDERS_FILE, orders)

            cart.clear()
            print("Заказ оформлен!")

        elif choice == "6":
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

def show_restaurant_menu():

    # Загрузка ресторанов
    restaurants = load_data(RESTAURANTS_FILE)

    # Проверка наличия ресторанов
    if not restaurants:
        print("Ресторанов пока нет")
        return

    print("\n=== ВЫБЕРИТЕ РЕСТОРАН ===")

    # Вывод списка ресторанов
    for index, restaurant in enumerate(restaurants, start=1):
        print(f"{index}. {restaurant['username']}")

    # Выбор ресторана
    restaurant_index = int(input("Номер ресторана: ")) - 1

    # Проверка корректности выбора
    if restaurant_index < 0 or restaurant_index >= len(restaurants):
        print("Неверный номер ресторана")
        return

    selected_restaurant = restaurants[restaurant_index]

    # Проверка наличия меню
    if not selected_restaurant["menu"]:
        print("У ресторана пока нет блюд")
        return

    print(f"\n=== МЕНЮ: {selected_restaurant['username']} ===")

    # Вывод меню ресторана
    for index, item in enumerate(selected_restaurant["menu"], start=1):

        print(
            f"{index}. "
            f"{item['name']} | "
            f"{item['category']} | "
            f"{item['price']} руб."
        )

def add_to_cart(cart):

    # Загрузка ресторанов
    restaurants = load_data(RESTAURANTS_FILE)

    # Проверка наличия ресторанов
    if not restaurants:
        print("Ресторанов пока нет")
        return

    print("\n=== ВЫБЕРИТЕ РЕСТОРАН ===")

    # Вывод ресторанов
    for index, restaurant in enumerate(restaurants, start=1):
        print(f"{index}. {restaurant['username']}")

    # Выбор ресторана
    restaurant_index = int(input("Номер ресторана: ")) - 1

    # Проверка выбора
    if restaurant_index < 0 or restaurant_index >= len(restaurants):
        print("Неверный номер ресторана")
        return

    selected_restaurant = restaurants[restaurant_index]

    # Проверка меню
    if not selected_restaurant["menu"]:
        print("У ресторана нет блюд")
        return

    print(f"\n=== МЕНЮ: {selected_restaurant['username']} ===")

    # Вывод меню
    for index, item in enumerate(selected_restaurant["menu"], start=1):

        print(
            f"{index}. "
            f"{item['name']} | "
            f"{item['category']} | "
            f"{item['price']} руб."
        )

    # Выбор блюда
    dish_index = int(input("Номер блюда: ")) - 1

    # Проверка выбора блюда
    if dish_index < 0 or dish_index >= len(selected_restaurant["menu"]):
        print("Неверный номер блюда")
        return

    selected_dish = selected_restaurant["menu"][dish_index]

    # Добавление блюда в корзину
    cart.append(selected_dish)

    print(f"Блюдо '{selected_dish['name']}' добавлено в корзину!")

def show_cart(cart):

    # Проверка пустой корзины
    if not cart:
        print("Корзина пуста")
        return

    print("\n=== КОРЗИНА ===")

    total_price = 0

    # Вывод товаров из корзины
    for index, item in enumerate(cart, start=1):

        print(
            f"{index}. "
            f"{item['name']} | "
            f"{item['category']} | "
            f"{item['price']} руб."
        )

        total_price += item["price"]

    # Итоговая стоимость
    print(f"\nИтоговая сумма: {total_price} руб.")

def show_client_orders(user):

    # Загрузка заказов
    orders = load_data(ORDERS_FILE)

    # Поиск заказов клиента
    client_orders = [
        order for order in orders
        if order["client"] == user["username"]
    ]

    # Проверка наличия заказов
    if not client_orders:
        print("У вас пока нет заказов")
        return

    print("\n=== МОИ ЗАКАЗЫ ===")

    # Вывод заказов
    for order in client_orders:

        print(f"\nID заказа: {order['id']}")
        print(f"Статус: {order['status']}")

        print("Блюда:")

        for item in order["items"]:

            print(
                f"- {item['name']} "
                f"({item['category']}) "
                f"- {item['price']} руб."
            )

        print(f"Сумма заказа: {order['total_price']} руб.")

def cancel_order(user):

    # Загрузка заказов
    orders = load_data(ORDERS_FILE)

    # Получение заказов клиента
    client_orders = [
        order for order in orders
        if order["client"] == user["username"]
    ]

    # Проверка наличия заказов
    if not client_orders:
        print("У вас нет заказов")
        return

    print("\n=== ВАШИ ЗАКАЗЫ ===")

    for order in client_orders:

        print(
            f"ID: {order['id']} | "
            f"Статус: {order['status']}"
        )

    order_id = int(input("Введите ID заказа: "))

    for order in orders:

        if (
            order["id"] == order_id and
            order["client"] == user["username"]
        ):

            # Проверка возможности отмены
            if order["status"] == "Доставлен":
                print("Нельзя отменить доставленный заказ")
                return

            # Изменение статуса
            order["status"] = "Отменён"

            save_data(ORDERS_FILE, orders)

            print("Заказ успешно отменён!")
            return

    print("Заказ не найден")

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