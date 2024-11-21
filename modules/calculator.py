class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль!")
            return None

    def calculate(self):
        while True:
            print("\n--- Калькулятор ---")
            print("1. Сложение (+)")
            print("2. Вычитание (-)")
            print("3. Умножение (*)")
            print("4. Деление (/)")
            print("5. История операций")
            print("6. Выход")

            choice = input("Выберите операцию: ")

            if choice == "1":
                self.perform_operation(self.add, "+")
            elif choice == "2":
                self.perform_operation(self.subtract, "-")
            elif choice == "3":
                self.perform_operation(self.multiply, "*")
            elif choice == "4":
                self.perform_operation(self.divide, "/")
            elif choice == "5":
                self.show_history()
            elif choice == "6":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")

    def perform_operation(self, operation, symbol):
        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))

            result = operation(num1, num2)
            if result is not None:
                print(f"Результат: {num1} {symbol} {num2} = {result}")
                self.history.append(f"{num1} {symbol} {num2} = {result}")
        except ValueError:
            print("Ошибка: Введите корректные числа.")

    def show_history(self):
        if not self.history:
            print("История пуста.")
        else:
            print("\n--- История операций ---")
            for entry in self.history:
                print(entry)
