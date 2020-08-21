# NAME

`citty`: Continuous Integration in a tty

# SYNOPSIS

    $ $EDITOR citty.py  # Configure your project directories

    $ python citty.py
    project1 | project2 | ...	# These have color!

# DESCRIPTION

Remember the mantra of Test-Driven Development (TDD)? 

  > Red, Green, Refactor!

Well, that's all I'm trying to do. So I wanted a CI driver that would run my
tests, show the status, and get out of the way!

`citty` runs in a terminal. It uses `\r` to refresh the same line over and over
again. And it prints the name of each project it knows about, in either
Coca-Cola RED, DeWalt YELLOW, or John Deere GREEN. And by "Coca-Cola",
"DeWalt", and "John Deere" I mean "ANSI".

## 1,000 words or more

Here's a video of `citty` running inside a `:terminal` window
in Gvim (version 8!), using three "projects" that are really
symlinks to the same directory. With the sleep time set to 5 seconds. And a `make test` that just
uses the Bash `$RANDOM` value to flip a coin to determine
success or failure. (But it's really colorful!)


![Video of citty running in Gvim](/etc/citty-in-gvim.gif?raw=true "Citty running in Gvim terminal")

## Coding

There is a subtle and nuanced coding system:

  * Green - It's all good!
  * Yellow - Running tests, please stand by.
  * Red - Shit's broke.

## Status

How do I determine the status? Using the result code returned from `make test`.

## Testing mechanisms

You can use any testing mechanism you like, as long at it's `make test`. 

Or, you could add a new feature to `citty.py`. I'll gladly read your PR,
but if it includes the words "XML" or "microservice" it's going right in the
trash.
