import json
import csv
from datetime import datetime


class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        data = {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }
        return data

    @staticmethod
    def from_dict(data):
        return FinanceRecord(
            id=data["id"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"],
        )


class FinanceManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.records = self.load_records()

    def load_records(self):
        """
        Загружает финансовые записи из JSON-файла. Если файл пустой или отсутствует, возвращает пустой список.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read()
                if not content:
                    return []
                return [
                    FinanceRecord.from_dict(record) for record in json.loads(content)
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_records(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [record.to_dict() for record in self.records],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def menu(self):
        while True:
            print("\n--- Управление финансовыми записями ---")
            print("1. Добавить финансовую запись")
            print("2. Просмотреть все записи")
            print("3. Фильтровать записи по дате или категории")
            print("4. Генерация отчёта")
            print("5. Импорт данных из CSV")
            print("6. Экспорт данных в CSV")
            print("7. Назад в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_record()
            elif choice == "2":
                self.view_all_records()
            elif choice == "3":
                self.filter_records()
            elif choice == "4":
                self.generate_report()
            elif choice == "5":
                self.import_from_csv()
            elif choice == "6":
                self.export_to_csv()
            elif choice == "7":
                break
            else:
                print("Неверный ввод, попробуйте снова.")

    def add_record(self):
        try:
            amount = float(
                input(
                    "Введите сумму операции (положительное число для дохода, отрицательное для расхода): "
                )
            )
            category = input(
                "Введите категорию операции (например, 'Еда', 'Транспорт'): "
            )
            date = input("Введите дату операции (в формате ДД-ММ-ГГГГ): ")
            description = input("Введите описание операции: ")

            new_record = FinanceRecord(
                id=len(self.records) + 1,
                amount=amount,
                category=category,
                date=date,
                description=description,
            )
            self.records.append(new_record)
            self.save_records()
            print("Финансовая запись добавлена!")
        except ValueError:
            print("Ошибка ввода. Убедитесь, что сумма указана корректно.")

    def view_all_records(self):
        if not self.records:
            print("Записи отсутствуют.")
            return

        print("\n--- Список всех финансовых записей ---")
        for record in self.records:
            print(
                f"[{record.id}] {record.date} | {record.category} | {'Доход' if record.amount > 0 else 'Расход'}: {record.amount} | {record.description}"
            )

    def filter_records(self):
        print("\n--- Фильтрация записей ---")
        print("1. Фильтровать по дате")
        print("2. Фильтровать по категории")
        choice = input("Выберите фильтр: ")

        if choice == "1":
            date = input("Введите дату для фильтрации (в формате ДД-ММ-ГГГГ): ")
            filtered = [record for record in self.records if record.date == date]
        elif choice == "2":
            category = input("Введите категорию для фильтрации: ")
            filtered = [
                record
                for record in self.records
                if record.category.lower() == category.lower()
            ]
        else:
            print("Неверный ввод.")
            return

        if not filtered:
            print("Записи не найдены.")
        else:
            for record in filtered:
                print(
                    f"[{record.id}] {record.date} | {record.category} | {'Доход' if record.amount > 0 else 'Расход'}: {record.amount} | {record.description}"
                )

    def generate_report(self):
        start_date = input("Введите начальную дату (в формате ДД-ММ-ГГГГ): ")
        end_date = input("Введите конечную дату (в формате ДД-ММ-ГГГГ): ")

        try:
            start_dt = datetime.strptime(start_date, "%d-%m-%Y")
            end_dt = datetime.strptime(end_date, "%d-%m-%Y")

            filtered = [
                record
                for record in self.records
                if start_dt <= datetime.strptime(record.date, "%d-%m-%Y") <= end_dt
            ]

            income = sum(record.amount for record in filtered if record.amount > 0)
            expenses = sum(record.amount for record in filtered if record.amount < 0)

            print("\n--- Отчёт ---")
            print(f"Доходы: {income}")
            print(f"Расходы: {expenses}")
            print(f"Баланс: {income + expenses}")
        except ValueError:
            print("Ошибка ввода дат. Убедитесь, что даты указаны корректно.")

    def import_from_csv(self):
        csv_file_path = input("Введите путь к CSV-файлу: ").strip()
        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    new_record = FinanceRecord.from_dict(
                        {
                            "id": len(self.records) + 1,
                            "amount": float(row["amount"]),
                            "category": row["category"],
                            "date": row["date"],
                            "description": row["description"],
                        }
                    )
                    self.records.append(new_record)
            self.save_records()
            print("Данные успешно импортированы!")
        except Exception as e:
            print(f"Ошибка при импорте: {e}")

    def export_to_csv(self):
        file_path = input("Введите путь для сохранения CSV-файла: ").strip()
        try:
            with open(file_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = ["id", "amount", "category", "date", "description"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.records:
                    writer.writerow(record.to_dict())
            print("Данные успешно экспортированы!")
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")
