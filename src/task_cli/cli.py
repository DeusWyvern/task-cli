import click
import json
import pathlib
import sys
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

    task_dictionary = {}
    this_task_id = 1

    if not file_path.is_file():
        open(file_path, "w").close()

    with open(file_path, "r") as openfile:
        try:
            task_dictionary = json.load(openfile)
            task_id_list = list(task_dictionary.keys())
            this_task_id = int(max(task_id_list)) + 1
        except json.JSONDecodeError:
            pass

    with open(file_path, "w") as openfile:
        new_task = {this_task_id: task}
        task_dictionary.update(new_task)
        json.dump(task_dictionary, openfile)

    click.echo(f"Added TASK <{task}> with ID <{this_task_id}> to file. Marked TODO.")


@cli.command()
@click.argument("id", type=click.INT)
@click.argument("task", type=click.STRING, metavar="<task name>")
def update(id, task):
    """Updates task with ID <id> to new task <task>."""

    file_path = FILE_PATH

    task_dictionary = {}
    string_id = str(id)

    if not file_path.is_file():
        open(file_path, "w").close()

    with open(file_path, "r+") as openfile:
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
    click.echo("Remove")
    click.echo(f"{id}")


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
