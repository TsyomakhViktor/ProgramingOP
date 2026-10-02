class Product:
    def __init__(self, product_id, name, price, stock):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def get_formatted_price(self):
        # Форматування ціни за вимогами: ххх.ххгрн
        return f"{self.price:.2f}грн"

    def __str__(self):
        return f"[{self.id}] {self.name:<15} — {self.get_formatted_price():<12} (На складі: {self.stock} шт.)"


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_subtotal(self):
        return self.product.price * self.quantity


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        if quantity <= 0:
            print("❌ Кількість товару має бути більше 0!")
            return

        # Перевірка скільки цього товару ВЖЕ у кошику (лямбда)
        in_cart_item = next(filter(lambda item: item.product.id == product.id, self.items), None)
        current_in_cart = in_cart_item.quantity if in_cart_item else 0

        if current_in_cart + quantity > product.stock:
            available = product.stock - current_in_cart
            print(f"❌ Недостатньо товару на складі! Доступно для додавання: {available} шт.")
            return

        if in_cart_item:
            in_cart_item.quantity += quantity
        else:
            self.items.append(CartItem(product, quantity))

        print(f"✅ Додано '{product.name}' ({quantity} шт.) до кошика.")

    def remove_product(self, product_id):
        initial_count = len(self.items)
        # Видалення з кошика через лямбда-фільтрацію
        self.items = list(filter(lambda item: item.product.id != product_id, self.items))

        if len(self.items) < initial_count:
            print("✅ Товар успішно видалено з кошика.")
        else:
            print("❌ Товар з таким ID не знайдено у вашому кошику.")

    def get_total_price(self):
        # Обчислення суми через sum + map + лямбда
        return sum(map(lambda item: item.get_subtotal(), self.items))

    def show_cart(self):
        if not self.items:
            print("\n🛒 Ваш кошик порожній.")
            return False

        fmt_price = lambda p: f"{p:.2f}грн"

        print("\n" + "=" * 45)
        print("                🛒 ВАШ КОШИК")
        print("=" * 45)
        for item in self.items:
            p = item.product
            print(f"ID: {p.id} | {p.name:<15} x{item.quantity:<3} = {fmt_price(item.get_subtotal())}")
        
        print("-" * 45)
        print(f"Загальна сума до сплати: {fmt_price(self.get_total_price())}")
        print("=" * 45)
        return True

    def clear(self):
        self.items.clear()


class Store:
    def __init__(self):
        self.products = [
            Product(1, "Клавіатура", 1250.00, 10),
            Product(2, "Мишка", 650.50, 15),
            Product(3, "Монітор", 5400.00, 4),
            Product(4, "Навушники", 1899.99, 7),
            Product(5, "Килимок", 350.00, 20)
        ]
        self.cart = ShoppingCart()
        self.admin_password = "admin"

    def show_catalog(self):
        print("\n" + "=" * 55)
        print("               📦 КАТАЛОГ ТОВАРІВ")
        print("=" * 55)
        for product in self.products:
            print(product)
        print("=" * 55)

    def process_purchase(self):
        if not self.cart.show_cart():
            return

        confirm = input("\nПідтвердити покупку? (1 - Так, 0 - Ні): ").strip()
        if confirm == "1":
            for item in self.cart.items:
                item.product.stock -= item.quantity

            fmt_price = lambda p: f"{p:.2f}грн"
            print(f"\n🎉 Покупка успішна! Оплачено: {fmt_price(self.cart.get_total_price())}")
            self.cart.clear()
        else:
            print("\n❌ Покупку скасовано.")

    def admin_panel(self):
        password = input("\nВведіть пароль адміністратора: ").strip()
        if password != self.admin_password:
            print("❌ Невірний пароль!")
            return

        print("\n" + "=" * 55)
        print("        🔐 ПАНЕЛЬ АДМІНІСТРАТОРА (ЗАЛИШКИ НА СКЛАДІ)")
        print("=" * 55)
        
        format_stock_line = lambda p: f"ID: {p.id:<2} | Назва: {p.name:<15} | Ціна: {p.get_formatted_price():<10} | Залишок: {p.stock} шт."
        for p in self.products:
            print(format_stock_line(p))
            
        print("=" * 55)


def main():
    store = Store()

    while True:
        print("\n" + "─" * 35)
        print("          ГОЛОВНЕ МЕНЮ")
        print("─" * 35)
        print("1. Переглянути каталог товарів")
        print("2. Додати товар в кошик")
        print("3. Переглянути / Видалити з кошика")
        print("4. Купити товари з кошика")
        print("5. Увійти як адміністратор")
        print("0. Вийти з програми")
        print("─" * 35)

        choice = input("Виберіть дію (0-5): ").strip()

        if choice == "1":
            store.show_catalog()
            input("\nНатисніть Enter, щоб повернутися в меню...")

        elif choice == "2":
            store.show_catalog()
            try:
                p_id = int(input("\nВведіть ID товару: "))
                # Використання лямбда-функції для пошуку за ID
                product = next(filter(lambda p: p.id == p_id, store.products), None)

                if product:
                    qty = int(input(f"Введіть кількість для '{product.name}': "))
                    store.cart.add_product(product, qty)
                else:
                    print("❌ Товару з таким ID не існує.")
            except ValueError:
                print("❌ Помилка введення! Вводьте тільки цілі числа.")
            
            input("\nНатисніть Enter, щоб повернутися в меню...")

        elif choice == "3":
            if store.cart.show_cart():
                action = input("\nБажаєте видалити товар з кошика? (1 - Так, 0 - Ні): ").strip()
                if action == "1":
                    try:
                        p_id = int(input("Введіть ID товару для видалення: "))
                        store.cart.remove_product(p_id)
                    except ValueError:
                        print("❌ Помилка введення! Введіть числовий ID.")
            
            input("\nНатисніть Enter, щоб повернутися в меню...")

        elif choice == "4":
            store.process_purchase()
            input("\nНатисніть Enter, щоб повернутися в меню...")

        elif choice == "5":
            store.admin_panel()
            input("\nНатисніть Enter, щоб повернутися в меню...")

        elif choice == "0":
            print("\nДякуємо за користування магазином! До побачення.")
            break

        else:
            print("❌ Невірний вибір. Оберіть пункт від 0 до 5.")


if __name__ == "__main__":
    main()