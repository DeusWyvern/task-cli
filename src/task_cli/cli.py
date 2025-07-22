import click
import pathlib
import sys
from datetime import datetime
from . import list_commands
from . import file_functions
from .constants import FILE_EXTENSION, DEFAULT_FILE_NAME

# Entry point for the CLI
@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--file', '-f', default=DEFAULT_FILE_NAME, help='Name of the file to store tasks in.')
@click.argument("path", type=click.Path(exists=True, file_okay=False, readable=True, path_type=pathlib.Path), metavar="<PATH>")
def cli(ctx, file, path):
    file_name = file + FILE_EXTENSION
    file_path = path.joinpath(file_name)
    if not file_path.is_file():
        file_functions.init_task_file(file_path)
        click.echo(f"File initialized at '{file_path}'")
    elif not ctx.invoked_subcommand:
        click.echo("No arguments provided.")
        sys.exit(1)

    ctx.obj = {}
    ctx.obj['path'] = file_path



@cli.command()
@click.argument("task", type=click.STRING, metavar="<task name>")
@click.pass_context
def add(ctx, task):
    """Adds a task called <task name> to the task list."""

    file_path = ctx.obj['path']
    add_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_id = 1

    tasks_file = file_functions.get_tasks(file_path)
    tasks_list = tasks_file['tasks']

    if tasks_list:
        id_list = list((task["id"] for task in tasks_list))
        new_id = max(id_list) + 1

    this_task = {
        "id": new_id,
        "description": task,
        "status": "todo",
        "createdAt": add_time,
        "updatedAt": add_time,
    }

    tasks_list.append(this_task)

    file_functions.write_tasks(file_path, tasks_file)
    click.echo(f"Added TASK <{task}> with ID <{this_task['id']}> to file. Marked TODO.")


@cli.command()
@click.argument("id", type=click.INT)
@click.argument("task", type=click.STRING, metavar="<task name>")
@click.pass_context
def update(ctx, id, task):
    """Updates task with ID <id> to new task <task name>."""

    file_path = ctx.obj['path']
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tasks_file = file_functions.get_tasks(file_path)
    tasks_list = tasks_file["tasks"]

    found_index = None

    for i, item in enumerate(tasks_list):
        if item["id"] == id:
            found_index = i
            break

    if found_index is None:
        click.echo("Cannot update. Task ID does not exist.")
        sys.exit(1)

    tasks_list[found_index]["description"] = task
    tasks_list[found_index]["updatedAt"] = update_time

    file_functions.write_tasks(file_path, tasks_file)

    click.echo(f"Task with ID {id} updated to '{task}'.")


@cli.command()
@click.argument("id", type=click.INT)
@click.pass_context
def delete(ctx, id):
    """Removes task with ID <id>."""

    file_path = ctx.obj['path']

    tasks_file = file_functions.get_tasks(file_path)
    tasks_list = tasks_file['tasks']

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

    file_functions.write_tasks(file_path, tasks_file)

    click.echo(f"Removed TASK '{found_task[1]['description']}' with ID {id}.")


@cli.command()
@click.argument("id", type=click.INT)
@click.pass_context
def mark_in_progress(ctx, id):
    """Mark task with ID <id> as in progress."""

    file_path = ctx.obj['path']

    tasks_file = file_functions.get_tasks(file_path)
    tasks_list = tasks_file["tasks"]

    found_task = None

    for i, item in enumerate(tasks_list):
        if item["id"] == id:
            found_task = (i, item)
            break

    if found_task is None:
        click.echo("Cannot update. Task ID does not exist.")
        sys.exit(1)

    found_index = found_task[0]

    tasks_list[found_index]["status"] = "in-progress"

    file_functions.write_tasks(file_path, tasks_file)

    click.echo(f"Task '{tasks_list[found_index]['description']}' with ID {id} marked in-progress.")




@cli.command()
@click.argument("id", type=click.INT)
@click.pass_context
def mark_done(ctx, id):
    """Mark task with ID <id> as done."""

    file_path = ctx.obj['path']

    tasks_file = file_functions.get_tasks(file_path)
    tasks_list = tasks_file["tasks"]

    found_task = None

    for i, item in enumerate(tasks_list):
        if item["id"] == id:
            found_task = (i, item)
            break

    if found_task is None:
        click.echo("Cannot update. Task ID does not exist.")
        sys.exit(1)

    found_index = found_task[0]

    tasks_list[found_index]["status"] = "done"

    file_functions.write_tasks(file_path, tasks_file)

    click.echo(f"Task '{tasks_list[found_index]['description']}' with ID {id} marked done.")

cli.add_command(list_commands.list)
