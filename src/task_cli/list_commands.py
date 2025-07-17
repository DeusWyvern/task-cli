import click


@click.group(invoke_without_command=True)
@click.pass_context
def list(ctx):
    """List all tasks. Can be filtered by flag."""
    if not ctx.invoked_subcommand:
        click.echo(f"List all {ctx.invoked_subcommand}")


@list.command()
def done():
    """List all tasks flagged as done."""
    click.echo("Done")


@list.command()
def todo():
    """List all tasks flagged as todo."""
    click.echo("Todo")


@list.command()
def in_progress():
    """List all tasks flagged still in-progress."""
    click.echo("In-progress")
