import time


class Note:
    def __init__(self):
        self.__note_id = -1
        self.__header = ""
        self.__text = ""
        self.__created = 0.0
        self.__modified = 0.0

    def set_id(self, note_id):
        self.__note_id = note_id

    def get_id(self):
        return self.__note_id

    def set_header(self, header):
        self.__header = header

    def get_header(self):
        return self.__header

    def set_text(self, text):
        self.__text = text

    def get_text(self):
        return self.__text

    def set_created(self, init):
        self.__created = init

    def get_created(self):
        return self.__created

    def set_modified(self, modified):
        self.__modified = modified

    def get_modified(self):
        return self.__modified

    def as_str(self):
        return (f"Note # {self.__note_id}\n"
                f"Header: {self.__header}\n"
                f"Text: {self.__text}\n"
                f"Created: {time.asctime(time.localtime(self.__modified))}\n"
                f"Modified: {time.asctime(time.localtime(self.__modified))}")

    def __repr__(self):
        return (f"Note (Id: {self.__note_id}, "
                f"Header: {self.__header}, "
                f"Modified: {time.asctime(time.localtime(self.__modified))})")
