#! /bini/env python

import os
import argparse
import random
import string

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
allcase = string.ascii_letters
digits = string.digits
charset = allcase + digits
selfname = os.path.basename(__file__)
ext = "txt"


def random_rename(length: int = 5, path: str = os.getcwd()):
    files = (
        file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
    )
    for file in files:
        if file == selfname:
            continue
        newname = generate_filename(charset, path, length)
        os.rename(file, newname)


def generate_filename(charset, path, length=None):
    if not length:
        length = random.choice(range(9, 12))
    name = "".join(random.choices(charset, k=length))
    while os.path.isfile(os.path.join(path, name + "." + ext)):
        name = "".join(random.choices(charset, k=length))
    return name + "." + ext


def argument_rename(name, path: str = os.getcwd()):
    files = (
        file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
    )
    last = 1
    for file in files:
        if file == selfname or file == name + "." + ext:
            continue
        newname = name
        while os.path.isfile(os.path.join(path, newname + "." + ext)):
            newname = f"{name}({last})"
            last += 1
        os.rename(file, newname + "." + ext)


argument_rename("donkey")
