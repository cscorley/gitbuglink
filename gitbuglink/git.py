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
            , bug_ids = detect(commit.message)
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
