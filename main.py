"""
для более-менее нормального отображения в PyCharm нужно
в Run/Debug Configurations активировать настройку Emulate terminal in output console
"""

from os import system

import adapter
import file
from filter import FilterModeMap, filter_notes, convert_required
from model import Model
from note import Note

model: Model
DATA_DIR_NAME = "data"
DATA_FILE_NAME = "notes.json"


def clear_terminal():
    system("cls")


def show_all():
    show_note_list(model.get_note_list(), "Notes list:")


def show_note_list(notes: list[Note], list_header):
    clear_terminal()
    print(list_header)
    if notes:
        for note in notes:
            print(note)
    else:
        print("no entries")
    input("Enter anything to continue...")


def show_note():
    clear_terminal()
    index = get_note_index()
    if index >= 0:
        clear_terminal()
        print(model.get_note(index).as_str())
    input("Enter anything to continue...")


def get_note_index() -> int:
    index = -1
    answer = input("Enter note id: ")
    if answer.isdigit():
        index = model.get_note_index(int(answer))
        if index < 0:
            print(f"Note with id {answer} not found")
    else:
        print(f"Incorrect id - {answer}!")
    return index


def add_note():
    clear_terminal()
    note_data = input_note_data("Add new note:")
    model.add_note(*note_data)
    write_file()


def write_file():
    file.backup_file(DATA_DIR_NAME, DATA_FILE_NAME)
    file.write_file(DATA_DIR_NAME, DATA_FILE_NAME,
                    adapter.list_to_json(model.get_note_list()))


def input_note_data(message):
    if message:
        print(message)
    header = input("Enter note header: ")
    text = input("Enter note text: ")
    return [header, text]


def find_note():
    clear_terminal()
    print("Select search mode:")
    fm_map = FilterModeMap.filter_mode_map
    for key in fm_map.keys():
        print(f"{key}. {fm_map[key]}")
    answer = input("or anything different to cancel: ")
    mode = fm_map.get(answer)
    if not mode:
        return

    answer = input(FilterModeMap.requirements_map[answer])
    required = convert_required(mode, answer)
    if required:
        note_list = filter_notes(model.get_note_list(), mode, required)
        show_note_list(note_list, f"Notes with \"{required}\" in {mode}:")
    else:
        print(f"Incorrect required \"{answer}\" for mode \"{mode}\"")
        input("Enter anything to continue...")


def edit_note():
    clear_terminal()
    index = get_note_index()
    if index >= 0:
        clear_terminal()
        note = model.get_note(index)
        print(note.as_str())

        note_data = input_note_data("\nEnter new values "
                                    "or empty line to keep old ones:")
        if note_data[0] or note_data[1]:
            if not note_data[0]:
                note_data[0] = note.get_header()
            elif not note_data[1]:
                note_data[1] = note.get_text()
            if model.edit_note(index, *note_data):
                write_file()
                clear_terminal()
                print("Successfully edited!\n")
                print(model.get_note(index).as_str())
            else:
                print("Something went wrong. Note isn't edited")
        else:
            print("No changes are made")
    input("Enter anything to continue...")


def delete_note():
    clear_terminal()
    index = get_note_index()
    if index >= 0:
        clear_terminal()
        note = model.get_note(index)
        print(note.as_str())
        confirm = input("\nEnter note index to confirm deletion: ")
        if confirm == str(note.get_id()):
            if model.delete_node(index):
                write_file()
                clear_terminal()
                print("Successfully deleted!\n")
            else:
                print("Something went wrong. Note isn't deleted")
        else:
            print("Note won't be deleted")
    input("Enter anything to continue...")


def main():
    global model

    if not file.ensure_path_exists(DATA_DIR_NAME, DATA_FILE_NAME):
        print(f"can't create data file (seems like directory with name \"{DATA_FILE_NAME}\" exists)")
        input("Enter anything to exit...")
        return

    note_list = adapter.json_to_list(file.read_file(DATA_DIR_NAME, DATA_FILE_NAME))
    model = Model()
    model.set_note_list(note_list)

    while True:
        clear_terminal()

        size = model.size()
        match size:
            case 0:
                entries = "no entries"
            case 1:
                entries = "1 entry"
            case _:
                entries = f"{size} entries"

        answer = input(f"Note book ({entries}):\n"
                       "1. Show notes list\n"
                       "2. Show note\n"
                       "3. Add a note\n"
                       "4. Find a note\n"
                       "5. Edit a note\n"
                       "6. Delete a note\n"
                       "7. Exit\n")
        match answer:
            case "1":
                show_all()
            case "2":
                show_note()
            case "3":
                add_note()
            case "4":
                find_note()
            case "5":
                edit_note()
            case "6":
                delete_note()
            case "7":
                return
            case _:
                print(f"Unknown command - {answer}!")
                input("Enter anything to continue...")


if __name__ == '__main__':
    main()
