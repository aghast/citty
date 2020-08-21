#! /usr/bin/env python3
# vim: fileencoding: utf-8
""" citty -- CI driver in your terminal.

    Implements basic test & wait continuous integration,
    and codes the results to stdout using color escape
    sequences.

    Usage:
      citty add <path> [--name=<name>] [-f | --force]
      citty delete <name>
      citty delete --all
      citty -h | --help
      citty --version
      citty

    Options:
      -f --force    Force it! Overwrite an old project if needed.
      -h --help     Show this screen.
      --name=<name> Project name (default: directory).
      --version     Show version.

"""
import json
import os
import platform
import subprocess
import sys
import time

from pathlib import Path

from docopt import docopt

__version__ = "0.0.1"

ON_WINDOWS = platform.system() == "Windows"

CITTY = "citty"
_CITTY = "_" + CITTY if ON_WINDOWS else "." + CITTY

ADD = "add"
APPDATA = "APPDATA"
COMMAND = "command"
DELETE = "delete"
FAILING = "FAILING"
MAKE_TEST = "make test"
NAME = "name"
NORMAL = "NORMAL"
PASSING = "PASSING"
PATH = "path"
PENDING = "PENDING"
PROJECTS = "projects"
SLEEP = "sleep"
SLEEP_TIME = 60
STATUS = "status"
VERSION = "citty version " + __version__
XDG_CONFIG_HOME = "XDG_CONFIG_HOME"


def citty_add(arguments):
    """ Add a project to citty config file. """
    assert arguments[ADD], "'citty add' should be the command line"
    assert arguments["<path>"], "<path> must be specified"
    name = arguments["--name"]
    path = Path(arguments["<path>"]).resolve()
    if not name:
        name = path.name
    config = load_config()
    if any(proj[NAME] == name for proj in config[PROJECTS]):
        if not arguments["--force"]:
            print("Cannot add '{}' -- that project already exists!".format(name))
            sys.exit(1)

        config[PROJECTS][:] = [d for d in config[PROJECTS] if d[NAME] != name]

    project = {NAME: name, PATH: str(path), COMMAND: MAKE_TEST, STATUS: PENDING}
    config[PROJECTS].append(project)
    save_config(config)


def citty_delete(arguments):
    """ Delete a project, or all projects, from the config. """
    assert arguments[DELETE], "'citty delete' must be specified"
    config = load_config()
    projects = config[PROJECTS]
    if arguments["--all"]:
        projects[:] = []
    else:
        name = arguments["<name>"]
        projects[:] = [p for p in projects if p[NAME] != name]
    save_config(config)


def citty_loop(arguments):
    """ Run a continuous-integration loop, forever. """
    config = load_config()
    while True:
        ci_build(config)
        time.sleep(config[SLEEP])


def config_file_path() -> Path:
    """ Determine and return the path to where the citty config file *should*
        be, whether it exists or not.

    """

    def path_ok(varname: str):
        nonlocal env
        path = Path(env.get(varname, ""))
        if path.is_dir():
            return path / CITTY
        return None

    env = os.environ

    path = path_ok(XDG_CONFIG_HOME)
    if path:
        return path

    path = path_ok(APPDATA)
    if path:
        return path

    path = Path.home()
    if path.is_dir():
        path /= _CITTY
        return path

    raise NotADirectoryError("Could not find a location to load/store" " config data.")


def load_config():
    """ Load json config file data, if file exists."""
    cfp = config_file_path()
    if not cfp.exists():
        return {SLEEP: SLEEP_TIME, PROJECTS: []}
    with open(cfp) as cfg:
        config = json.load(cfg)
    config[PROJECTS].sort(key=lambda x: x[NAME])
    return config


def save_config(config):
    """ Write json config file data. """
    cfp = config_file_path()
    with open(cfp, "w") as cf:
        json.dump(config, cf)


def make_test(project):
    """ Run 'make test' to determine CI status. """
    kwargs = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if project[PATH] is not None:
        kwargs["cwd"] = project[PATH]

    argv_list = """make test""".strip().split()
    try:
        rc = subprocess.run(argv_list, **kwargs)
        retcode = rc.returncode
    except OSError as e:
        print("Error: could not start build of project '{}'".format(project[NAME]))
        print(e)
        retcode = 2

    return retcode


ESC_BGCOLOR = "\x1B[{};48;5;{}m"


def show_status(config):
    """ Print project names with corresponding background color. """
    colors = {
        FAILING: ESC_BGCOLOR.format(37, 196),
        PASSING: ESC_BGCOLOR.format(30, 46),
        PENDING: ESC_BGCOLOR.format(30, 228),
        NORMAL: "\x1B[40;37m",
    }

    stats = [
        "{} {} {}".format(colors[proj[STATUS]], proj[NAME], colors[NORMAL])
            for proj in config[PROJECTS]
    ]
    stats_line = " | ".join(stats)
    print(stats_line, end="\r")


def ci_build(config):
    """ Do one pass through all projects, updating status. """
    test_funcs = {
        MAKE_TEST: make_test,
    }

    for project in config[PROJECTS]:
        project[STATUS] = PENDING
        show_status(config)
        command = project[COMMAND]
        rc = test_funcs[command](project)
        project[STATUS] = PASSING if rc == 0 else FAILING
        show_status(config)


def main():
    arguments = docopt(__doc__, version=VERSION)

    ops = {
        ADD: citty_add,
        DELETE: citty_delete,
    }

    for cmd, fn in ops.items():
        if arguments[cmd]:
            fn(arguments)
            break
    else:
        citty_loop(arguments)


if __name__ == "__main__":
    main()
