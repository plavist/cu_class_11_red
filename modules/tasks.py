import json
import csv


class Task:
    def __init__(
        self, id, title, priority="Средний", description="", done=False, due_date=None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def mark_done(self):
        self.done = True

    def edit(self, title=None, description=None, priority=None, due_date=None):
        if title:
            self.title = title
        if description:
            self.descirption = description
        if priority:
            self.priority = priority
        if due_date:
            self.due_date = due_date

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.descirption,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date,
        }
        return data

    @staticmethod
    def from_dict(data):
        task = Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            done=data.get("done", False),
            priority=data.get("priority", "Средний"),
            due_date=data["due_date"],
        )
        return task


class TasksManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def add_task(self):
        title = input("Введите заголовок задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Введите приоритет задачи (Высокий/Средний/Низкий): ")
        due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")

        new_task = Task(
            id=len(self.tasks) + 1,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача добавлена!")

    def view_tasks(self):
        if not self.tasks:
            print("Нет доступных задач.")
            return

        print("\nСписок задач:")
        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(
                f"[{task.id}] {task.title} | Приоритет: {task.priority} | Срок: {task.due_date} | Статус: {status}"
            )

    def mark_task_done(self):
        task_id = int(input("Введите ID задачи: "))
        task = next((task for task in self.tasks if task.id == task_id), None)

        if not task:
            print("Задача не найдена.")
            return

        task.mark_done()
        self.save_tasks()
        print("Задача отмечена как выполненная!")

    def edit_task(self):
        task_id = int(input("Введите ID задачи для редактирования: "))
        task = next((task for task in self.tasks if task.id == task_id), None)

        if not task:
            print("Задача не найдена.")
            return

        new_title = input(f"Введите новый заголовок (текущий: {task.title}): ").strip()
        new_description = input(
            f"Введите новое описание (текущее: {task.description}): "
        ).strip()
        new_priority = input(
            f"Введите новый приоритет (текущий: {task.priority}): "
        ).strip()
        new_due_date = input(f"Введите новый срок (текущий: {task.due_date}): ").strip()

        task.edit(
            title=new_title,
            description=new_description,
            priority=new_priority,
            due_date=new_due_date,
        )
        self.save_tasks()
        print("Задача обновлена!")

    def delete_task(self):
        task_id = int(input("Введите ID задачи для удаления: "))
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        print("Задача удалена!")

    def import_from_csv(self):
        csv_file_path = input("Введите путь к CSV-файлу: ")
        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    new_task = Task.from_dict(
                        {
                            "id": len(self.tasks) + 1,
                            "title": row["title"],
                            "description": row["description"],
                            "done": row["done"].lower() == "true",
                            "priority": row["priority"],
                            "due_date": row["due_date"],
                        }
                    )
                    self.tasks.append(new_task)
            self.save_tasks()
            print("Задачи успешно импортированы!")
        except Exception as e:
            print(f"Ошибка при импорте: {e}")

    def export_to_csv(self):
        file_path = input("Введите путь для сохранения CSV-файла: ")
        try:
            with open(file_path, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = [
                    "id",
                    "title",
                    "description",
                    "done",
                    "priority",
                    "due_date",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for task in self.tasks:
                    writer.writerow(task.to_dict())
            print("Задачи успешно экспортированы!")
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")

    def menu(self):
        while True:
            print("\n--- Управление задачами ---")
            print("1. Добавить задачу")
            print("2. Просмотреть задачи")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Импорт задач из CSV")
            print("7. Экспорт задач в CSV")
            print("8. Назад в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.mark_task_done()
            elif choice == "4":
                self.edit_task()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                self.import_from_csv()
            elif choice == "7":
                self.export_to_csv()
            elif choice == "8":
                break
            else:
                print("Неверный ввод, попробуйте снова.")
