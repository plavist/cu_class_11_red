from datetime import datetime
import json
import csv


class Note:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def edit(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
        }
        return data

    @staticmethod
    def from_dict(data):
        note = Note(
            id=data["id"],
            title=data["title"],
            content=data["content"],
        )
        return note


class NotesManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return [Note.from_dict(note) for note in json.load(file)]
        except json.JSONDecodeError:
            return []
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(
                [note.to_dict() for note in self.notes],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def create_note(self):
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        new_note = Note(id=len(self.notes) + 1, title=title, content=content)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена!")

    def view_notes(self):
        if not self.notes:
            print("Нет доступных заметок.")
            return
        print("\nСписок заметок:")
        for note in self.notes:
            print(f"[{note.id}] {note.title} ({note.timestamp})")

    def view_note_details(self):
        note_id = int(input("Введите ID заметки: "))
        note = next((note for note in self.notes if note.id == note_id), None)
        if not note:
            print("Заметка не найдена...")
            return
        print("\nДетали заметки:")
        print(f"Заголовок: {note.title}")
        print(f"Содержимое: {note.content}")
        print(f"Дата создания/изменения: {note.timestamp}")

    def edit_note(self):
        note_id = int(input("Введите ID заметки для редактирования: "))
        note = next((note for note in self.notes if note.id == note_id), None)

        if not note:
            print("Заметка не найдена...")
            return

        new_title = input(f"Введите новый заголовок (текущий: {note.title}): ").strip()
        new_content = input(
            f"Введите новое содержимое (текущее: {note.title}): "
        ).strip()

        note.edit(title=new_title, content=new_content)

        self.save_notes()
        print("Заметка обновлена!")

    def delete_note(self):
        note_id = int(input("Введите ID заметки для удаления: "))
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()
        print("Заметка успешно удалена!")

    def import_from_csv(self):
        csv_file_path = input("Введите путь к CSV-файлу: ").strip()
        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    new_note = Note.from_dict(
                        {
                            "id": len(self.notes) + 1,
                            "title": row["title"],
                            "content": row["content"],
                            "timestamp": row["timestamp"],
                        }
                    )
                    self.notes.append(new_note)
            self.save_notes()
            print("Заметки успешно импортированы!")
        except Exception as e:
            print(f"Ошибка при импорте: {e}")

    def export_to_csv(self):
        csv_file_path = input("Введите путь для сохранения CSV-файла: ").strip()
        try:
            with open(csv_file_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = ["id", "title", "content", "timestamp"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for note in self.notes:
                    writer.writerow(note.to_dict())
            print("Заметки успешно экспортированы!")
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")

    def menu(self):
        while True:
            print("\n--- Управление заметками ---")
            print("1. Создать заметку")
            print("2. Просмотреть все заметки")
            print("3. Просмотреть заметку подробно")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Импорт заметок из CSV")
            print("7. Экспорт заметок в CSV")
            print("8. Назад в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_note()
            elif choice == "2":
                self.view_notes()
            elif choice == "3":
                self.view_note_details()
            elif choice == "4":
                self.edit_note()
            elif choice == "5":
                self.delete_note()
            elif choice == "6":
                self.import_from_csv()
            elif choice == "7":
                self.export_to_csv()
            elif choice == "8":
                break
            else:
                print("Неверный ввод, попробуйте снова.")
