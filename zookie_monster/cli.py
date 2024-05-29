"""This module provides the Zookie Monster CLI."""
# zookie_monster/cli.py

from typing import Optional

import typer

from zookie_monster import __app_name__, __version__, crawler


app = typer.Typer()

@app.command()
def crawl(
	base_url: str = typer.Option(
		None,
		"--base-url",
		"-u",
		prompt="Base url to start crawl from"
	)
) -> None:
	crawler.crawl_site(base_url)
	return typer.Exit()

def _version_callback(value: bool) -> None:
	if value:
		typer.echo(f"{__app_name__} v{__version__}")
		raise typer.Exit()

@app.callback()
def main(
	version: Optional[bool] = typer.Option(
		None,
		"--version",
		"-v",
		help="Show the application's version and exit.",
		callback=_version_callback,
		is_eager=True,
	),
) -> None:
	return
