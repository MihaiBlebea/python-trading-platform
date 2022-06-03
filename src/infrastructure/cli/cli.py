import click
from src.di_container import Container

@click.group()
def main():
    """
    Simple CLI for querying books on Google Books by Oyetoke Toby
    """
    pass

@main.command()
@click.option("--username", "-u", type=str)
@click.option("--email", "-e", type=str)
@click.option("--password", "-p", type=str)
def account_register(username: str, email: str, password: str):
	if username is None:
		click.echo("please provide username")
		return

	if email is None:
		click.echo("please provide valid email")
		return

	if password is None:
		click.echo("please provide password")
		return

	click.echo("Command account-register running") 

	account = Container.account_auth.register(username, email, password)
	click.echo(account)


@main.command()
@click.option("--email", "-e", type=str)
@click.option("--password", "-p", type=str)
def account_login(email: str, password: str):
	if email is None:
		click.echo("please provide valid email")
		return

	if password is None:
		click.echo("please provide password")
		return

	click.echo("Command account-login running") 

	account = Container.account_auth.login(email, password)
	click.echo(account)

@main.command()
def fill_orders():
	click.echo("Command fill-orders running") 

	Container.order_execute.execute_all_pending()

	click.echo("Orders filled") 

if __name__ == "__main__":
	main()