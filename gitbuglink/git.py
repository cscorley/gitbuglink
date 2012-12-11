#!/usr/bin/env python2
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

from __future__ import (print_function, with_statement)

import re
import sys
import os
from collections import namedtuple
from optparse import OptionParser, SUPPRESS_HELP

import dulwich

TraceInfo = namedtuple('traceinfo', 'commit_id author committer date message bug_ids')
trigger_words = "bug|fix|pr|br|bz|bugzilla|issue|problem"
bugids = re.compile("(?:" + trigger_words + ")\\s*(?:id|[#=])?\\s*([0-9]{4,6})",
        flags=re.IGNORECASE)
plurals = re.compile("(?:" + trigger_words + ")s\\s*(?:id|[#=])?\\s*([0-9]{4,6})",
        flags=re.IGNORECASE)
idnumbers = re.compile("(?:id|[#=])\\s*([0-9]{4,6})", flags=re.IGNORECASE)
numbers = re.compile("([0-9]{4,6})", flags=re.IGNORECASE)
bugzillaURLs = re.compile("(?:http|https)://\S+/show_bug.cgi\?id=([0-9]{4,6})")

def detect(msg):
    ids = set()

    r = plurals.findall(msg)
    if r:
        # handle lists a bit differently
        lines = msg.split('\n')
        for line in lines:
            r = plurals.findall(line)
            if r:
                nr = numbers.findall(line)
                if nr:
                    ids.update(nr)

    r = bugids.findall(msg)
    if r:
        ids.update(r)

    r = bugzillaURLs.findall(msg)
    if r:
        ids.update(r)

    if len(ids) == 0:
        r = idnumbers.findall(msg)
        if r:
            ids.update(r)

    return tuple(ids)


def get_links(project_url):
    repo = dulwich.repo.Repo(project_url)

    for walk_entry in repo.get_walker():
        commit = walk_entry.commit

        trace = TraceInfo(
                author = commit.author
                , committer = commit.committer
                , commit_id = commit.id
                , date = commit.commit_time # + commit.commit_time_zone ?
                , message = commit.message
                , bug_ids = detect(commit.message)
                )

        yield trace


def process_humans(l, h, project_url):
    repo = dulwich.repo.Repo(project_url)

    for line in h:
        items = line.strip().split(',')
        commit = repo[items[0]]
        items = items[1:]
        confirmed_ids = list()

        print(">> Processing commit:", commit.id)
        print(commit.message)

        print("---------------------------------------------------")
        print(">> Which are the valid ids?", items)
        while True and len(items) > 0:
            for index, item in enumerate(items):
                print("%d) %s" %(index, item))
            print("q) None of these")

            response = raw_input("? ")
            if response == 'q':
                break
            i = int(response)

            print("Adding (%d) %s to links file." % (i, items[i]))
            confirmed_ids.append(items[i])
            items.remove(items[i])

        if len(confirmed_ids) > 0:
            l.write(commit.id + "," + ",".join(confirmed_ids) + "\n")


def main(argv):
    # Configure option parser
    optparser = OptionParser(usage='%prog [options] PATH', version='0.1')
    optparser.set_defaults(links_file='links.csv')
    optparser.set_defaults(humans_file='humans.csv')
    optparser.set_defaults(processing=False)
    optparser.add_option('-l', '--links_file', dest='links_file',
            help='Output file for links')
    optparser.add_option('-m', '--humans_file', dest='humans_file',
            help='Output file for human links')
    optparser.add_option('-p', '--process', dest='process',
            help='Process the humans file, appending results to the links file.', action='store_true')
    (options, args) = optparser.parse_args(argv)

    if len(args) > 1:
        repo = args[1]
    else:
        repo = "."

    if options.process:
        # for each in humans_file,
        #   display commit
        #   display list of detected ids
        #   input corrected list
        #   append result to links_file

        with open(options.links_file, 'a') as l:
            with open(options.humans_file, 'r') as h:
                process_humans(l, h, repo)

        return

    if os.path.exists(repo):
        with open(options.links_file, 'w') as l:
            with open(options.humans_file, 'w') as h:
                for each in get_links(repo):
                    if len(each.bug_ids) > 1:
                        h.write(each.commit_id + "," + ",".join(each.bug_ids) + "\n")
                    elif len(each.bug_ids) == 1:
                        l.write(each.commit_id + "," + each.bug_ids[0] + "\n")

    else:
        print("Path does not exist: ", repo)

if __name__ == '__main__':
    main(sys.argv)
