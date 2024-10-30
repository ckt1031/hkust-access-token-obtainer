import sys
import json


def get_path() -> str:
    # Check if argment defined file path
    return sys.argv[1] if len(sys.argv) > 1 else "data.json"


def save_file(data: dict):
    path = get_path()

    # data to json string
    data = json.dumps(data)

    # Save the data to a file
    with open(path, "w") as f:
        f.write(str(data))


def load_file() -> dict:
    path = get_path()

    # Load the data from a file
    with open(path, "r") as f:
        return json.loads(f.read())
