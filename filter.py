import time

from note import Note


class FilterModeMap:
    ID = "Id"
    HDR = "Header"
    TXT = "Text"
    CRT = "Creation time"
    MDF = "Modification time"

    filter_mode_map = {
        "1": ID,
        "2": HDR,
        "3": TXT,
        "4": CRT,
        "5": MDF,
    }

    requirements_map = {
        "1": "Enter note id as number: ",
        "2": "Enter note header to find: ",
        "3": "Enter note text to find: ",
        "4": "Enter note creation date in format YYYY-MM-DD: ",
        "5": "Enter note modification date in format YYYY-MM-DD: ",
    }


def convert_required(mode: str, required: str):
    converted = None
    if required:
        match mode:
            case FilterModeMap.ID:
                if required.isdigit():
                    converted = required
            case FilterModeMap.HDR | FilterModeMap.TXT:
                converted = required
            case FilterModeMap.CRT | FilterModeMap.MDF:
                try:
                    converted = time.mktime(time.strptime(required, "%Y-%m-%d"))
                except ValueError:
                    pass
    return converted


def filter_notes(note_list: list[Note], mode: str, required) -> list[Note]:
    new_list = []
    match mode:
        case FilterModeMap.ID:
            new_list = list(filter(lambda note: required in str(note.get_id()), note_list))
        case FilterModeMap.HDR:
            new_list = list(filter(lambda note: required in note.get_header(), note_list))
        case FilterModeMap.TXT:
            new_list = list(filter(lambda note: required in note.get_text(), note_list))
        case FilterModeMap.CRT:
            max_required = required + 86400
            new_list = list(filter(lambda note: required <= note.get_created() < max_required, note_list))
        case FilterModeMap.MDF:
            max_required = required + 86400
            new_list = list(filter(lambda note: required <= note.get_modified() < max_required, note_list))

    return new_list
