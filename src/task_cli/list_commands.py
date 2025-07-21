import click
import sys
from . import file_functions
from . import list_functions

@click.group(invoke_without_command=True)
@click.pass_context
def list(ctx):
    """List all tasks. Can be filtered by flag."""
    if not ctx.invoked_subcommand:
        file_path = ctx.obj['path']
        tasks_file = file_functions.get_tasks(file_path)
        tasks = tasks_file['tasks']
        for task in tasks:
            task_string = list_functions.format_task(task)
            click.echo(task_string)
        sys.exit(0)



@list.command()
@click.pass_context
def done(ctx):
    """List all tasks flagged as done."""
    filter = 'done'
    file_path = ctx.obj['path']
    tasks_file = file_functions.get_tasks(file_path)
    tasks = tasks_file['tasks']
    filtered_tasks = list_functions.filter_tasks(tasks, filter)

    for task in filtered_tasks:
        task_string = list_functions.format_task(task)
        click.echo(task_string)


@list.command()
@click.pass_context
def todo(ctx):
    """List all tasks flagged as todo."""
    filter = 'todo'
    file_path = ctx.obj['path']
    tasks_file = file_functions.get_tasks(file_path)
    tasks = tasks_file['tasks']
    filtered_tasks = list_functions.filter_tasks(tasks, filter)

    for task in filtered_tasks:
        task_string = list_functions.format_task(task)
        click.echo(task_string)

@list.command()
@click.pass_context
def in_progress(ctx):
    """List all tasks flagged still in-progress."""
    filter = 'in-progress'
    file_path = ctx.obj['path']
    tasks_file = file_functions.get_tasks(file_path)
    tasks = tasks_file['tasks']
    filtered_tasks = list_functions.filter_tasks(tasks, filter)

    for task in filtered_tasks:
        task_string = list_functions.format_task(task)
        click.echo(task_string)
