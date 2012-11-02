#!/usr/bin/env python2.6
#
# [The "New BSD" license]
# Copyright (c) 2012 The Board of Trustees of The University of Alabama
# All rights reserved.
#
# See LICENSE for details.

import re
from collections import namedtuple

import dulwich

TraceInfo = namedtuple('traceinfo', 'commit_id parent_commit_id author committer date message bug_ids')
SuperRe = re.compile("(?:bug|fix|pr|br)\\s*(?:id|[#=])?\\s*([0-9]{4,6})")
# what about "Bug" "PR" and urls?

def detect(commit):
    ids = list()
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
            , bug_ids = detect(commit)
            )

        yield trace
