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
def restaurant_menu(user):
    while True:
        print("\n=== РЕСТОРАН ===")
        print("1. Посмотреть заказы")
        print("2. Изменить статус")
        print("0. Назад")

        choice = input("Выбор: ")

        orders = load_data(ORDERS_FILE)

        if choice == "1":
            for o in orders:
                print(o)

        elif choice == "2":
            order_id = int(input("ID заказа: "))
            new_status = input("Новый статус (Принят/Готовится/Готов к выдаче): ")

            for o in orders:
                if o["id"] == order_id:
                    o["status"] = new_status

            save_data(ORDERS_FILE, orders)


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