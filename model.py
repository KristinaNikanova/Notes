import time

from note import Note


def timestamp() -> float:
    return time.time()


class Model:

    def __init__(self):
        self.__note_list = []
        self.__last_id = 0

    def set_note_list(self, note_list: list[Note]):
        self.__note_list = note_list
        if self.__note_list:
            self.__last_id = self.__note_list[-1].get_id()

    def get_note_list(self) -> list[Note]:
        return self.__note_list

    def size(self) -> int:
        return len(self.__note_list)

    def add_note(self, header: str, text: str):
        note = Note()
        note.set_header(header)
        note.set_text(text)
        _timestamp = timestamp()
        note.set_created(_timestamp)
        note.set_modified(_timestamp)
        self.__note_list.append(note)
        self.__last_id += 1
        note.set_id(self.__last_id)

    def get_note_index(self, note_id: int) -> int:
        for i in range(self.size()):
            if self.__note_list[i].get_id() == note_id:
                return i
        return -1

    def get_note(self, index: int) -> Note | None:
        if index not in range(self.size()):
            return None
        return self.__note_list[index]

    def edit_note(self, index: int, header: str, text: str) -> bool:
        if index not in range(self.size()):
            return False
        note = self.__note_list[index]
        note.set_header(header)
        note.set_text(text)
        note.set_modified(timestamp())
        return True

    def delete_node(self, index: int) -> bool:
        if index not in range(self.size()):
            return False
        del self.__note_list[index]
        return True
