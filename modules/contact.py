import json
import csv


class Contact:
    def __init__(self, id, name, phone, email=""):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def edit(self, name=None, phone=None, email=None):
        if name:
            self.name = name
        if phone:
            self.phone = phone
        if email:
            self.email = email

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }
        return data

    @staticmethod
    def from_dict(data):
        contact = Contact(
            id=data["id"],
            name=data["name"],
            phone=data["phone"],
            email=data.get("email", ""),
        )
        return contact


class ContactManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.data_path, "r") as file:
                content = file.read().strip()
                if not content:
                    return []
                return [Contact.from_dict(contact) for contact in json.loads(content)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        with open(self.data_path, "w") as file:
            json.dump(
                [contact.to_dict() for contact in self.contacts],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def add_contact(self):
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите email (необязательно): ")

        new_contact = Contact(
            id=len(self.contacts) + 1, name=name, phone=phone, email=email
        )
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт добавлен!")

    def search_contact(self):
        query = input("Введите имя или номер телефона для поиска: ").lower()
        results = [
            contact
            for contact in self.contacts
            if query in contact.name.lower() or query in contact.phone
        ]

        if not results:
            print("Контакты не найдены.")
            return

        print("\nНайденные контакты:")
        for contact in results:
            print(
                f"[{contact.id}] {contact.name} | Телефон: {contact.phone} | Email: {contact.email}"
            )

    def edit_contact(self):
        id = int(input("Введите ID контакта для редактирования: "))
        contact = next((contact for contact in self.contacts if contact.id == id), None)

        if not contact:
            print("Контакт не найден.")
            return

        new_name = input(f"Введите новое имя (текущее: {contact.name}): ").strip()
        new_phone = input(f"Введите новый телефон (текущий: {contact.phone}): ").strip()
        new_email = input(f"Введите новый email (текущий: {contact.email}): ").strip()

        contact.edit(name=new_name, phone=new_phone, email=new_email)
        self.save_contacts()
        print("Контакт обновлен!")

    def delete_contact(self):
        id = int(input("Введите ID контакта для удаления: "))
        self.contacts = [contact for contact in self.contacts if contact.id != id]
        self.save_contacts()
        print("Контакт удален!")

    def import_from_csv(self):
        csv_file_path = input("Введите путь к CSV-файлу: ").strip()
        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    new_contact = Contact.from_dict(
                        {
                            "id": len(self.contacts) + 1,
                            "name": row["name"],
                            "phone": row["phone"],
                            "email": row["email"],
                        }
                    )
                    self.contacts.append(new_contact)
            self.save_contacts()
            print("Контакты успешно импортированы!")
        except Exception as e:
            print(f"Ошибка при импорте: {e}")

    def export_to_csv(self):
        csv_file_path = input("Введите путь для сохранения CSV-файла: ")
        try:
            with open(csv_file_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = ["id", "name", "phone", "email"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for contact in self.contacts:
                    writer.writerow(contact.to_dict())
            print("Контакты успешно экспортированы!")
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")

    def menu(self):
        while True:
            print("\n--- Управление контактами ---")
            print("1. Добавить контакт")
            print("2. Поиск контакта")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Импорт контактов из CSV")
            print("6. Экспорт контактов в CSV")
            print("7. Назад в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.search_contact()
            elif choice == "3":
                self.edit_contact()
            elif choice == "4":
                self.delete_contact()
            elif choice == "5":
                self.import_from_csv()
            elif choice == "6":
                self.export_to_csv()
            elif choice == "7":
                break
            else:
                print("Неверный ввод, попробуйте снова.")
