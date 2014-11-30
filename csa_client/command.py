import click

@click.group()
def cli():
    pass

@cli.command()
def login():
    click.echo('Not implemented')
