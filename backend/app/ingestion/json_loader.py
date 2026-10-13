import json

def load_json(file_path: str):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.dumps(
            json.load(f),
            indent=2
    )