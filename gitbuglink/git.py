#!/usr/bin/env python2.6
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
import csv
from collections import namedtuple

import dulwich

TraceInfo = namedtuple('traceinfo', 'commit_id author committer date message bug_ids')
bugre = re.compile("(?:bug|fix|pr|br|bz)\\s*(?:id|[#=])?\\s*([0-9]{4,6})",
        flags=re.IGNORECASE)
bzurlre = re.compile("(?:http|https)://\S+/show_bug.cgi\?id=([0-9]{4,6})",
        flags=re.IGNORECASE)
# what about "Bug" "PR", multiple ids, and urls?

def detect(commit):
    ids = set()
    ids.update(detect_message(commit.message))
    # filter by time?
    return tuple(ids)

def detect_message(msg):
    returning = list()

    r = bugre.findall(msg)
    if r:
        returning.extend(r)

    r = bzurlre.findall(msg)
    if r:
        returning.extend(r)

    return returning


def get_links(project_url):
    count = 0
    repo = dulwich.repo.Repo(project_url)

    for walk_entry in repo.get_walker():
        commit = walk_entry.commit

        trace = TraceInfo(
            author = commit.author
            , committer = commit.committer
            , commit_id = commit.id
            , date = commit.commit_time # + commit.commit_time_zone ?
            , message = commit.message
            , bug_ids = detect(commit)
            )

        yield trace

def main(args):
    for p in args[1:]:
        if os.path.exists(p):
            for each in get_links(args[1]):
                if len(each.bug_ids) > 1:
                    print("Human, what do you think? ", each.commit_id + "," + str(each.bug_ids))
                elif len(each.bug_ids) == 1:
                    print("A wild link appears!", each.commit_id + "," + str(each.bug_ids[0]))

        else:
            print("Path does not exist: ", p)

if __name__ == '__main__':
    main(sys.argv)
