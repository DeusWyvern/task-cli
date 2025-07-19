import click
import json
import pathlib
import sys
from datetime import datetime
from . import list_commands

# Hard code file name and path for tests. To be removed.
CURRENT_PATH = pathlib.Path().resolve()
FILE_NAME = "test.json"
FILE_PATH = CURRENT_PATH.joinpath(FILE_NAME)


# Entry point for the CLI
@click.group()
def cli():
    pass


@cli.command()
@click.argument("task", type=click.STRING, metavar="<task name>")
def add(task):
    """Adds a task called <name> to the task list."""

    file_path = FILE_PATH
    add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task_dictionary = {"tasks": []}

    if not file_path.is_file():
        with open(file_path, "w") as newfile:
            json.dump(task_dictionary, newfile)

    with open(file_path, "r") as readfile:
        try:
            file_contents = json.load(readfile)
            task_dictionary = file_contents
        except json.JSONDecodeError:
            pass

    new_id = 1

    if task_dictionary["tasks"]:
        id_list = list((object["id"] for object in task_dictionary["tasks"]))
        new_id = max(id_list) + 1

    this_task = {
        "id": new_id,
        "description": task,
        "status": "todo",
        "createdAt": add_time,
        "updatedAt": add_time,
    }

    task_dictionary["tasks"].append(this_task)

    with open(file_path, "w") as writefile:
        json.dump(task_dictionary, writefile)

    click.echo(f"Added TASK <{task}> with ID <{this_task['id']}> to file. Marked TODO.")


@cli.command()
@click.argument("id", type=click.INT)
@click.argument("task", type=click.STRING, metavar="<task name>")
def update(id, task):
    """Updates task with ID <id> to new task <task>."""

    file_path = FILE_PATH

    if not file_path.is_file():
        open(file_path, "w").close()

    with open(file_path, "r+") as openfile:
        task_dictionary = {}
        string_id = str(id)
        try:
            task_dictionary = json.load(openfile)
        except json.JSONDecodeError:
            pass

        if string_id not in task_dictionary.keys():
            click.echo("Cannot update. Task ID does not exist.")
            sys.exit(1)

        task_dictionary[string_id] = task

        openfile.seek(0)
        json.dump(task_dictionary, openfile)
        openfile.truncate()

    click.echo(f"Task with ID {id} updated to '{task}.")


@cli.command()
@click.argument("id", type=click.INT)
def delete(id):
    """Removes task with ID <id>."""
    file_path = FILE_PATH

    removed_task = None

    if not file_path.is_file():
        open(file_path, "w").close()
        click.echo(f"Task with ID {id} does not exist.")
        sys.exit(1)

    with open(file_path, "r+") as openfile:
        task_dictionary = {}

        try:
            task_dictionary = json.load(openfile)
        except json.JSONDecodeError:
            pass

        task_list = list(task_dictionary.values())
        task_id_index = id - 1
        removed_task = task_list.pop(task_id_index)

        task_dictionary_updated = {}

        for i, task in enumerate(task_list):
            task_dictionary_updated[i + 1] = task

        openfile.seek(0)
        json.dump(task_dictionary_updated, openfile)
        openfile.truncate()

    click.echo(f"Removed TASK '{removed_task}' with ID {id}.")


@cli.command()
@click.argument("id", type=click.INT)
def mip(id):
    """Mark task with ID <id> as in progress."""
    click.echo("Mark in-progress")
    click.echo(f"{id}")


@cli.command()
@click.argument("id", type=click.INT)
def md(id):
    """Mark task with ID <id> as done."""
    click.echo("Mark done")
    click.echo(f"{id}")


cli.add_command(list_commands.list)
