import click
import datetime
import json
import sys
from functools import update_wrapper
from tabulate import tabulate

from requests.exceptions import HTTPError
from token_cache import TokenCache
from api import CsaAPI

NOW = datetime.datetime.now()

def sort_json(json_data, key):
    """Sort a list of json by a given key """
    return sorted(json_data, key=lambda x:x[key])

def update_non_empty(json_data, update_data):
    """Update a dict with another dict where the value is not None """
    json_data.update((k, v) for k, v in update_data.iteritems()
                        if v is not None)
    return json_data

def print_multiple_entries(json_data, show_keys):
    """Print a table of json data to the cli"""
    header = [key for key in show_keys]
    table_data = [[item[key]  for key in show_keys] for item in json_data]

    table_string = tabulate(table_data, headers=header, tablefmt="rst")
    click.echo(table_string)

def catch_HTTPError(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
       try:
           return ctx.invoke(f, ctx, *args, **kwargs)
       except HTTPError, e:
           click.echo(e)
           sys.exit(1)
    return update_wrapper(new_func, f)

@click.group()
@click.pass_context
def cli(ctx):
    if not ctx.invoked_subcommand == 'authorize':
        try:
            ctx.obj = CsaAPI()
        except ValueError, e:
            click.echo(e)
            click.echo("Could not retrieve tokens from cache. "
                       "Have you run csa_client authorize ?")
            sys.exit(1)
        except HTTPError, e:
            click.echo(e.message)
            sys.exit(1)

@cli.command()
@click.option('--username', prompt='Enter your username',
              help="Username used to connect to the CsaAPI")
@click.password_option(help="Password used to connect to the CsaAPI")
@click.pass_context
@catch_HTTPError
def authorize(ctx, username, password):
    try:
        ctx.obj = CsaAPI(username=username, password=password)
    except HTTPError, e:
        click.echo(e.message)
        sys.exit(1)

##############################################################################
# User's group commands
##############################################################################

@cli.group()
@click.pass_context
@catch_HTTPError
def users(ctx):
    """Users group init function"""
    pass

@users.command()
@click.argument("query")
@click.option('--sort-by', default='id',
              type=click.Choice(['id', 'firstname', 'surname', 'email']))
@click.pass_context
@catch_HTTPError
def search(ctx, query, sort_by):
    """ Search for users """
    users_list = ctx.obj.search(query)
    users_list = sort_json(users_list, sort_by)
    print_multiple_entries(users_list, ['id', 'firstname', 'surname', 'email', 'phone'])

@users.command()
@click.argument("user-id")
@click.pass_context
@catch_HTTPError
def show(ctx, user_id):
    """ Search for users """
    user = ctx.obj.get_user(user_id)
    print_multiple_entries([user], ['id', 'firstname', 'surname', 'email', 'phone'])

@users.command()
@click.option('--firstname', prompt="Enter firstname",
              help="Firstname of the user")
@click.option('--surname', prompt="Enter surname",
              help="Surname of the user")
@click.option('--email', prompt="Enter email",
              help="Email address of the user")
@click.option('--grad_year', prompt="Enter grad year",
              type=click.IntRange(1970, NOW.year),
              help="Year of graduation")
@click.option('--jobs', is_flag=True, expose_value=True,
              prompt='Do has a job?',
              help="Whether the user subscribes to jobs")
@click.option('--login', prompt="Enter login",
              help="Login name for the user")
@click.password_option('--password', help="Password for the user")
@click.pass_context
@catch_HTTPError
def create(ctx, **user_params):
    ctx.obj.create_user(user_params)
    click.echo("User created.")

@users.command()
@click.argument('id', type=int)
@click.option('--firstname', help="Firstname of the user")
@click.option('--surname', help="Surname of the user")
@click.option('--email', help="Email address of the user")
@click.option('--grad_year', type=click.IntRange(1970, NOW.year),
              help="Year of graduation")
@click.option('--jobs', is_flag=True, expose_value=True,
              help="Whether the user subscribes to jobs")
@click.pass_context
@catch_HTTPError
def update(ctx, **user_params):
    user = ctx.obj.get_user(user_params['id'])
    user = update_non_empty(user, user_params)
    ctx.obj.update_user(user)
    click.echo("User updated.")

@users.command()
@click.argument('user-id', type=int)
@click.pass_context
@catch_HTTPError
def destroy(ctx, user_id):
    ctx.obj.destroy_user(user_id)
    click.echo("User destoryed.")

##############################################################################
# Broadcast's group commands
##############################################################################

@cli.group()
@click.pass_context
def broadcasts(ctx):
    """Users group init function"""
    pass

@broadcasts.command()
@click.argument('content', type=str)
@click.option('--feeds', '-f', multiple=True, type=str)
@click.pass_context
@catch_HTTPError
def create(ctx, content, feeds):
    user = ctx.obj.get_user()
    broadcast = {'user_id': user['id'], 'content': content}
    broadcast_params = {'broadcast': broadcast, 'feeds': feeds}
    ctx.obj.create_broadcast(broadcast_params)
    click.echo("Broadcast created.")

@broadcasts.command()
@click.pass_context
@catch_HTTPError
def show(ctx):
    """ Search for users """
    broadcasts_list = ctx.obj.get_broadcasts()
    print_multiple_entries(broadcasts_list, ['user_id', 'content', 'url'])

@broadcasts.command()
@click.argument('broadcast-id', type=int)
@click.pass_context
@catch_HTTPError
def destroy(ctx, broadcast_id):
    ctx.obj.destroy_broadcast(broadcast_id)
    click.echo("Broadcast destoryed.")

if __name__ == "__main__":
    cli(obj={})
