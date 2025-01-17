# Zookie Monster

## About

### What is Zookie Monster?
Just like a zombified Cookie Monster, it's a crawler that's cookie driven. It crawls in search of cookies.
![fbcb2c13f9c40f3926ba862727c0d3c7](https://github.com/sjstark/zookie-monster/assets/6759557/cd3cf680-9ff9-456b-83c8-633b1b544101)


## How to Use

### Installation
Install requirements with:

```console
$ python3 -m pip install -r requirements.txt
```

### Run Tests
```console
$ python3 -m pytest tests/
```

## Developing

### Dependencies

[Typer](https://typer.tiangolo.com/) Used to help structure CLI commandline tool interface. Provides application decorators

[Pytest](https://docs.pytest.org/en/8.2.x/) Used to test application development.

[Shellingham](https://pypi.org/project/shellingham/) Used to detect what shell the current Python executable is running in.

[Colorama]() Used to create ANSI escape character sequences (for colored terminal text and cursor positioning)
