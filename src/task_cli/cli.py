import click
from .list_commands import list


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name", type=click.STRING)
def add(name):
    """Adds a task called <name> to the task list."""
    click.echo(name)


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


cli.add_command(list)
