# NAME

`citty`: Continuous Integration in a tty

# SYNOPSIS

    ## Install

    $ python setup.py develop   # local

    $python setup.py install    # global

    ## Add projects

    $ citty add ~/projects/foo  # "name" is foo

    $ citty add ~/projects/foo --name fubar  # "name" is "fubar"

    ## List projects
    $ citty list
                foo : make test  : ~/projects/foo
              fubar : make test  : ~/projects/foo

    $ citty list fubar		# match name or path
              fubar : make test  : ~/projects/foo

    ## Delete projects

    $ citty delete foo          # exact name match

    $ citty list
              fubar : make test  : ~/projects/foo

    $ citty delete --all	# delete ALL the projects


    ## Run CI in your TTY
    $ citty
    project1 | fubar       	# <-- displayed in colors

# DESCRIPTION

Remember the mantra of Test-Driven Development (TDD)? 

  > Red, Green, Refactor!

Well, that's all I'm trying to do. So I wanted a CI driver that would run my
tests, show the status, and get out of the way!

`citty` runs in a terminal. It uses `\r` to refresh the same line over and over
again. And it prints the name of each project it knows about, in either
Coca-Cola RED, DeWalt YELLOW, or John Deere GREEN. (And by "Coca-Cola",
"DeWalt", and "John Deere" I mean "ANSI".)

## 1,000 words or more

Here's a video of `citty` running inside a `:terminal` window
in Gvim (version 8!), using three "projects" that are really
symlinks to the same directory. With the sleep time set to 5 seconds. And a `make test` that just
uses the Bash `$RANDOM` value to flip a coin to determine
success or failure. (Useless, but colorful in citty!)


![Video of citty running in Gvim](/etc/citty-in-gvim.gif?raw=true "Citty running in Gvim terminal")

## Coding

There is a subtle and nuanced coding system:

  * Green - Failure is not an option!
  * Yellow - Hold my beer while I pass these tests!
  * Red - It turns out, failure *is* an option!

## Status

How do I determine the status? Using the result code returned from `make test`.

## Testing mechanisms

You can use any testing mechanism you like, as long at it's `make test`. 

Or, you could add a new feature to `citty.py`. I'll gladly read your PR,
but if it includes the words "XML" or "microservice" it's going right in the
trash.
