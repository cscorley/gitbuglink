gitbuglink
=======

The stupid commit-bug traceability linker for the stupid content tracker

Requirements
============

The aim for `gitbuglink` is to be as stupid as possible. Other
multi-layered approaches exist (e.g.,
[MLink](http://home.engineering.iastate.edu/~anhnt/Research/MLink/index.php)),
but `gitbuglink` is not meant to replace those. At the moment,
`gitbuglink` will only use a series of regular expressions to determine
the link.

For input, `gitbuglink` accepts a file path to a local git repository.
It uses the `dulwich` Python module to access the repository log. Output
is a couple CSV files:

1. CSV of `(commit id, bug id)` tuples for confirmed links
2. CSV of `(commit id, bug id_1, bug id_2, ..., bug id_n)` tuples for
   links that require some form of human knowledge to establish the
   correct link.

Alternatively, if you use `gitbuglink` as a module in your Python tool,
then you will be able to access these links directly.

Initial support for link finding will work for Bugzilla bug
repositories. Additional repository types (e.g., JIRA, github issues)
should be able to be easily added.

But my subject system uses CVS/Subversion/...
=============================================

Well then, there are a few things out there for you:

1. Search for an (un)official project git mirror of the repository
2. [Use a conversion tool](http://lmgtfy.com/?q=cvs+to+git):
    1. [cvs2git](http://cvs2svn.tigris.org/cvs2git.html)
    2. [svn2git](https://github.com/nirvdrum/svn2git)
    3. (Send pull request for links to other tools you can recommend)

