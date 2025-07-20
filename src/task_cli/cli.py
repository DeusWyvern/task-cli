import click
import pathlib
import sys
from datetime import datetime
from . import list_commands
from . import file_functions

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
    """Adds a task called <task name> to the task list."""

    file_path = FILE_PATH
    add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not file_path.is_file():
        file_functions.init_task_file(file_path)
        click.echo("File initialized.")

    task_dictionary = file_functions.get_tasks(file_path)

    new_id = 1

    if task_dictionary["tasks"]:
        id_list = list((task["id"] for task in task_dictionary["tasks"]))
        new_id = max(id_list) + 1

    this_task = {
        "id": new_id,
        "description": task,
        "status": "todo",
        "createdAt": add_time,
        "updatedAt": add_time,
    }

    task_dictionary["tasks"].append(this_task)

    file_functions.write_tasks(file_path, task_dictionary)
    click.echo(f"Added TASK <{task}> with ID <{this_task['id']}> to file. Marked TODO.")


@cli.command()
@click.argument("id", type=click.INT)
@click.argument("task", type=click.STRING, metavar="<task name>")
def update(id, task):
    """Updates task with ID <id> to new task <task name>."""

    file_path = FILE_PATH
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not file_path.is_file():
        file_functions.init_task_file(file_path)
        click.echo("File initialized. Not tasks in file.")
        sys.exit(1)

    tasks = file_functions.get_tasks(file_path)
    tasks_list = tasks["tasks"]

    found_task = None

    for i, item in enumerate(tasks_list):
        if item["id"] == id:
            found_task = (i, item)
            break

    if found_task is None:
        click.echo("Cannot update. Task ID does not exist.")
        sys.exit(1)

    found_index = found_task[0]

    tasks_list[found_index]["description"] = task
    tasks_list[found_index]["updatedAt"] = update_time

    file_functions.write_tasks(file_path, tasks)

    click.echo(f"Task with ID {id} updated to '{task}.")


@cli.command()
@click.argument("id", type=click.INT)
def delete(id):
    """Removes task with ID <id>."""
    file_path = FILE_PATH

    if not file_path.is_file():
        file_functions.init_task_file(file_path)
        click.echo("File initialized. No tasks.")
        sys.exit(1)

    tasks = file_functions.get_tasks(file_path)
    tasks_list = tasks['tasks']

    found_task = None
    new_id = 1

    for i, item in enumerate(tasks_list):
        if item["id"] == id:
            found_task = (i, item)
        else:
            item['id'] = new_id
            new_id += 1

    if found_task is None:
        click.echo("Cannot delete. Task ID does not exist.")
        sys.exit(1)

    tasks_list.pop(found_task[0])

    file_functions.write_tasks(file_path, tasks)

    click.echo(f"Removed TASK '{found_task[1]['description']}' with ID {id}.")


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
