import click
import manta_client as mc

class RunGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        return None


@click.command(cls=RunGroup, invoke_without_command=True)
@click.version_option(version=mc.__version__)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
