gitbuglink
=======

The stupid commit-bug traceability linker for the stupid content tracker

The aim for gitbuglink is to be as stupid as possible. Other
multi-layered approaches exist (e.g.,
[MLink](http://home.engineering.iastate.edu/~anhnt/Research/MLink/index.php)),
but gitbuglink is not meant to replace those. At the moment,
gitbuglink will only use a series of regular expressions to determine
the link.

Initial support for link finding will work for Bugzilla bug
repositories. Additional repository types (e.g., JIRA, github issues)
should be able to be easily added (it may find a few accidentally).

If you find a commit message that was not linked, please send a pull
request with the appropriate test case. Please include a project repo url
and commit id in the comment of the test.

Usage
=====

For input, gitbuglink accepts a file path to a local git repository.
It uses the `dulwich` Python module to access the repository log. Output
is a couple CSV files:

1. `links.csv` -- a CSV of `(commit id, bug id)` for confirmed links
2. `humans.csv` -- a CSV of `(commit id, bug id_1, bug id_2, ..., bug id_n)` 
   for links that require some form of human knowledge to establish the
   correct link(s). The tool makes no assumptions about a commit when it finds
   multiple links. You should investigate the commit message yourself to
   confirm or correct the output.


But my subject system uses CVS/Subversion/...
=============================================

1. I don't care. Send a pull request when you get it working.
2. Search for an (un)official project git mirror of the repository
3. [Use a conversion tool](http://lmgtfy.com/?q=cvs+to+git):
    1. [cvs2git](http://cvs2svn.tigris.org/cvs2git.html)
    2. [svn2git](https://github.com/nirvdrum/svn2git)
    3. (Send pull request for links to other tools you can recommend)

