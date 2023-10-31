import time
from pathlib import Path

ENCODING = "utf-8"
BCKP_PREFIX = "backup"
MAX_BCKP_COUNT = 3


def ensure_path_exists(dir_name: str, file_name: str) -> bool:
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    path = Path(dir_name, file_name)
    if not path.exists():
        path.write_text("{}", encoding=ENCODING)
    elif path.is_dir():
        return False
    return True


def read_file(dir_name: str, file_name: str) -> str:
    path = Path(dir_name, file_name)
    if path.exists():
        return path.read_text(encoding=ENCODING)
    return ""


def write_file(dir_name: str, file_name: str, data: str):
    path = Path(dir_name, file_name)
    path.write_text(data, encoding=ENCODING)


def backup_file(dir_name: str, file_name: str):
    dir_path = Path(dir_name)
    if dir_path.exists():
        backup_files_list = list(dir_path.glob(f"{BCKP_PREFIX}*.bak"))
        backup_files_list.sort()
        while len(backup_files_list) >= MAX_BCKP_COUNT:
            Path(backup_files_list[0]).unlink()
            backup_files_list = backup_files_list[1:]

        _timestamp = time.strftime("%d%m%Y%H%M%S", time.localtime(time.time()))
        backup_path = Path(dir_name, f"{BCKP_PREFIX}{_timestamp}.bak")
        Path(dir_name, file_name).rename(backup_path)
