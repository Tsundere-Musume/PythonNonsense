#! /bin/env python
"""
Usage: ./create.py user [options]
       ./create.py rand [options]
       ./create.py {user,rand} --help
       """

import argparse
import random
import string
from pathlib import Path


# Renames the files of a given directory with random names
def random_rename(charset, path, length=None):
    selfname = Path(__file__)  # Path to the current python file
    files = path_validator(path).iterdir()  # An object with all the files

    for file in files:
        # Skips the file if it is a directory or it is this python file
        if not file.is_file() or file == selfname:
            continue
        # Renaming the old file with a new file
        newname = generate_filename(file.parent, file.suffixes, charset, length)
        file.rename(newname)


# Renames the file of a given directory with the name given as its argument
def argument_rename(name, path):
    selfname = Path(__file__)  # Path to the current python file
    files = path_validator(path).iterdir()  # An object with all the files

    for file in files:
        # Skips the file if it is a directory or it is this python file
        if not file.is_file() or file == selfname:
            continue
        # Appends a number if a file exists with the name provided
        # otherwise uses the name provided
        newname = get_valid_name(file.parent, name, file.suffixes)
        file.rename(newname)


# Returns a random name
def generate_filename(path, ext, charset, length):
    extensions = "".join(ext)  # Extensions to append to the new file name
    if not length:
        length = random.choice(range(9, 12))
    name = "".join(random.choices(charset, k=length)) + extensions
    # Generates a new file name if the file name already exists
    while (path / name).exists():
        name = "".join(random.choices(charset, k=length)) + extensions
    return path/name


# Appends a digit to a file if the file already exists
def get_valid_name(path, name, ext):
    extensions = "".join(ext)
    digit = 1
    new_name = name + extensions
    while (path / new_name).exists():
        new_name = f"{name}({digit}){extensions}"
    return path/new_name


# checks if a path is valid or not and returns the absolute path if valid
def path_validator(path):
    abs_path = Path(path).expanduser().resolve()
    if not abs_path.is_dir():
        print("Error: Path not valid. Try a valid path")
        exit(-1)
    return abs_path


# Determines what letters to use while renaming the files
def determineCharset(option):
    options = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "allcase": string.ascii_letters,
        "digits": string.digits,
        "alphanumeric": string.ascii_letters + string.digits,
    }
    return options.get(option, string.ascii_letters + string.digits)


# Arguments parser
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command")

# Commands for user mode
user = subparser.add_parser("user")
user.add_argument("word", type=str, help="The word to rename to.")
user.add_argument(
    "--path",
    "-p",
    type=str,
    help="Path to the directory [Defaults to the current directory]",
)

# Commands for the random mode
rand = subparser.add_parser("rand")
rand.add_argument("--length", "-l", type=int, help="Length for the random file names.")
rand.add_argument(
    "--charset",
    "-c",
    type=str,
    help="Things to include in the file name",
    choices=["lowercase", "uppercase", "allcase", "alphanumeric", "digits"],
)
rand.add_argument(
    "--path",
    "-p",
    type=str,
    help="Path to the directory [Defaults to the current directory]",
)
args = parser.parse_args()


if __name__ == "__main__":
    if args.command == "user":
        path = path_validator(args.path or ".")
        argument_rename(args.word, path=path)
    elif args.command == "rand":
        path = path_validator(args.path or ".")
        charset = determineCharset(args.charset or "default")
        length = args.length
        random_rename(charset, path, length)
