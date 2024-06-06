import json
import os
import sys


def out_file(content: str, path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, 'w') as f:
        f.write(content)


def parse_json(content: str) -> dict:
    try:
        return json.loads(content)
    except Exception as ex:
        print('Parse error: {}'.format(ex))
        sys.exit(5)


def get_obj(path: str) -> dict:
    return parse_json(content=get_content(path=path))


def get_content(path: str) -> str:
    with open(path) as f:
        return f.read()
