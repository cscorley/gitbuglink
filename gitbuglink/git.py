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
SuperRe = re.compile("(?:bug|fix|pr|br)\\s*(?:id|[#=])?\\s*([0-9]{4,6})")
# what about "Bug" "PR", multiple ids, and urls?

def detect(commit):
    ids = list()
    ids.append(detect_message(commit.message))
    # filter by time?
    return tuple(ids)

def detect_message(msg):
    r = SuperRe.match(msg)
    if r:
        return r.group(1)


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
                if each.bug_ids[0] is not None:
                    print(each.commit_id + "," + each.bug_ids[0])
        else:
            print("Path does not exist: ", p)

if __name__ == '__main__':
    main(sys.argv)
