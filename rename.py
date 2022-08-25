#! /bin/env python
"""
Usage: ./create.py user [options]
       ./create.py rand [options]
       ./create.py {user,rand} --help
       """

import os
import argparse
import random
import string
from pathlib import Path

# not renaming the file
selfname = __file__


# renames all the files in a directory with random names
def random_rename(path=os.getcwd()):
    files = (
        file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
    )
    for file in files:
        nfile = os.path.join(path, file)
        if nfile == selfname:
            continue
        ext = extension_grabber(file)
        newname = generate_filename(charset, path, ext, length)
        os.rename(nfile, newname)


# returns a random name
def generate_filename(charset, path, ext, length=None):
    if not length:
        length = random.choice(range(9, 12))
    name = "".join(random.choices(charset, k=length))
    while os.path.isfile(os.path.join(path, name + ext)):
        name = "".join(random.choices(charset, k=length))
    return os.path.join(path, name + ext)


# renames according to the user provided argument
def argument_rename(name, path=os.getcwd()):
    files = (
        file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
    )
    last = 1
    for file in files:
        ext = extension_grabber(file)
        nfile = os.path.join(path, file)
        if nfile == selfname or file == name + ext:
            continue
        newname = name
        while os.path.isfile(os.path.join(path, newname + ext)):
            newname = f"{name}({last})"
            last += 1
        os.rename(nfile, os.path.join(path, newname + ext))


# checks if a path is valid or not
def path_validator(path):
    epath = os.path.expanduser(path)
    if not os.path.isdir(epath):
        print("Error: Path not valid. Try a valid path")
        exit()
    return epath


# returns the extension of a file
def extension_grabber(file):
    return "".join(Path(file).suffixes)


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
        path = path_validator(args.path or os.getcwd())
        argument_rename(args.word, path=path)
    elif args.command == "rand":
        path = path_validator(args.path or os.getcwd())
        charset = determineCharset(args.charset or "default")
        length = args.length
        random_rename(path)
