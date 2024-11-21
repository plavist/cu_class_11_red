from modules.notes import NotesManager
from modules.contact import ContactManager
from modules.notes import NotesManager
from modules.tasks import TasksManager
from modules.calculator import Calculator


def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            manage_notes()
        elif choice == "2":
            manage_tasks()
        elif choice == "3":
            manage_contacts()
        elif choice == "4":
            manage_financial_records()
        elif choice == "5":
            calculator()
        elif choice == "6":
            print("Спасибо за использование Персонального помощника. До свидания!")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие от 1 до 6.")


def manage_notes():
    notes_manager = NotesManager("data/notes.json")
    notes_manager.menu()


def manage_tasks():
    task_manager = TasksManager("data/tasks.json")
    task_manager.menu()


def manage_contacts():
    contact_manager = ContactManager("data/contacts.json")
    contact_manager.menu()


def manage_financial_records():
    notes_manager = NotesManager("data/notes.json")
    notes_manager.menu()


def calculator():
    calculator = Calculator()
    calculator.calculate()


if __name__ == "__main__":
    main_menu()
