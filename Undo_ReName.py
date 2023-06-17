import json
import os


def undo_rename(json_path: str):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            rename_list = json.load(f)
    return rename_list


if __name__ == "__main__":
    rename_list = undo_rename("media_rename.json")
    print(rename_list)
    for old_path, new_path in rename_list:
        if old_path != new_path:
            if os.path.exists(new_path):
                os.rename(new_path, old_path)
