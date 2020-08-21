#! /usr/bin/env python3
# vim: fileencoding: utf-8
""" citty.py -- CI driver in your terminal.

    Implements basic test & wait continuous integration,
    and codes the results to stdout using color escape
    sequences.
"""
import os
import pathlib
import subprocess
import time

PROJECTS = [ ".", "../myproj", "../myproj2" ]
SLEEP_TIME = 60

ESC_BGCOLOR = "\x1B[{};48;5;{}m"
BG_RED = ESC_BGCOLOR.format(37, 196)
BG_GREEN = ESC_BGCOLOR.format(30, 46)
BG_YELLOW = ESC_BGCOLOR.format(30, 228)
BWHITE_BLACK = "\x1B[40;37m"

COLORS = {
    "RED": BG_RED,
    "GREEN": BG_GREEN,
    "YELLOW": BG_YELLOW,
    "NORMAL": BWHITE_BLACK,
    None: BG_YELLOW,
}

def get_projects():
    projects = {}

    for ppath in PROJECTS:

        name = pathlib.Path(ppath).name
        if not name:
            name = pathlib.Path(ppath).resolve().name

        print(ppath, " name = ", name)
        projects[name] = {
            "path": ppath,
            "status": None,
        }

    return projects


def make_test(wd):
    if wd is not None:
        os.chdir(wd)

    argv_list = """make test""".strip().split()
    rc = subprocess.run(argv_list, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    return rc.returncode


def show_status(projects):
    stats = ["{} {} {}".format(
                COLORS[proj.get("status")],
                name,
                BWHITE_BLACK)
            for name, proj in projects.items()]

    stats_line = " | ".join(stats)
    print(stats_line, end="\r")


def main():
    projects = get_projects()
    while True:
        for proj, info in projects.items():
            info["status"] = "YELLOW"
            show_status(projects)
            rc = make_test(info["path"])
            info["status"] = "GREEN" if rc == 0 else "RED"
            time.sleep(1)
            show_status(projects)
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
