import json
from .constants import TASKS_DICTIONARY

INDENT = 4

def init_task_file(file_path):
    with open(file_path, "w") as newfile:
        json.dump(TASKS_DICTIONARY, newfile, indent=INDENT)


def get_tasks(file_path):
    tasks = TASKS_DICTIONARY
    with open(file_path, "r") as openfile:
        try:
            tasks = json.load(openfile)
        except json.JSONDecodeError:
            pass
    return tasks


def write_tasks(file_path, tasks):
    with open(file_path, "w") as openfile:
        json.dump(tasks, openfile, indent=INDENT)
