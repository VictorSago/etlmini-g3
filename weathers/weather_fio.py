import json


def read_json_file(filepath, file_name="data.json"):
    file_path = filepath + "/" + file_name
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    #print(type(raw_data))
    return data


def save_json_file(data, filepath, file_name="data.json"):
    """A function that takes a Python dict and a filepath
    and saves the dict as a JSON object in that path"""
    file_path = filepath + "/" + file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
