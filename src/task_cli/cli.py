import click
import json
import pathlib
from . import list_commands


# Entry point for the CLI
@click.group()
def cli():
    pass


@cli.command()
@click.argument("name", type=click.STRING)
def add(name):
    """Adds a task called <name> to the task list."""

    current_path = pathlib.Path().resolve()
    file_name = "test.json"
    file_path = current_path.joinpath(file_name)

    task_dictionary = {}
    this_task_id = 1

    if not file_path.is_file():
        open(file_path, "w").close()

    with open(file_path, "r") as openfile:
        try:
            task_dictionary = json.load(openfile)
            task_id_list = list(task_dictionary.keys())
            this_task_id = int(max(task_id_list)) + 1
        except json.JSONDecodeError as e:
            click.echo(f"{e}")

    with open(file_path, "w") as openfile:
        new_task = {this_task_id: name}
        task_dictionary.update(new_task)
        json.dump(task_dictionary, openfile)

    click.echo(f"Added TASK <{name}> with ID <{this_task_id}> to file. Marked TODO.")


@cli.command()
@click.argument("id", type=click.INT)
@click.argument("task", type=click.STRING, metavar="<task name>")
def update(id, task):
    """Updates task with ID <id> to new task <task>."""
    click.echo(f"Update: '{task}'")
    click.echo(f"{id}")


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
