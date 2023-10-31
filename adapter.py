import json
from json import JSONDecodeError

from note import Note

__ID_KEY = "id"
__HDR_KEY = "header"
__TXT_KEY = "text"
__CRTD_KEY = "created"
__MDFD_KEY = "modified"


def list_to_json(note_list: list[Note]) -> str:
    jsonlist = []
    for note in note_list:
        jsonlist.append({
            __ID_KEY: note.get_id(),
            __HDR_KEY: note.get_header(),
            __TXT_KEY: note.get_text(),
            __CRTD_KEY: note.get_created(),
            __MDFD_KEY: note.get_modified(),
        })
    return json.dumps(jsonlist, indent=4)


def json_to_list(data_str: str) -> list[Note]:
    data = []
    try:
        data = json.loads(data_str)
    except JSONDecodeError:
        pass
    note_list = []
    for item in data:
        note = Note()
        note.set_id(item[__ID_KEY])
        note.set_header(item[__HDR_KEY])
        note.set_text(item[__TXT_KEY])
        note.set_created(item[__CRTD_KEY])
        note.set_modified(item[__MDFD_KEY])
        note_list.append(note)
    return note_list
