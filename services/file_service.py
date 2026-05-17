import json
import os

def load_data(filename):
    # Автоматическое создание файла, если он отсутствует
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)