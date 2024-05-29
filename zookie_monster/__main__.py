#!/usr/bin/python
"""Zookie Monster entry point script."""
# zookie_monster/__main__.py

from zookie_monster import cli, __app_name__, crawler
from typing_extensions import Annotated
import typer

def main(
		base_url: Annotated[str, typer.Argument(help="The base url to start webcrawl from. Should include protocol.")]
	):
	crawler.crawl_site(base_url)
	return typer.Exit()

if __name__ == "__main__":
	typer.run(main)
