#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (print_function, with_statement)

import re
import sys
import os
import csv
from collections import namedtuple

import dulwich.repo
import click

TraceInfo = namedtuple('traceinfo', 'commit_id author committer date message bug_ids')
trigger_words = "bug|fix|fixing|pr|br|bz|bugzilla|issue|problem"
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


def get_links(repo):

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


def process_humans(l, h, repo):
    # for each in humans_file,
    #   display commit
    #   display list of detected ids
    #   input corrected list
    #   append result to links_file

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


@click.command()
@click.option('--process', is_flag=True)
@click.option('--links_file', default='links.csv',
              help='Output file for links')
@click.option('--humans_file', default='humans.csv',
              help='Output file for links humans need to check')
@click.argument('git_path', type=click.Path(exists=True))
def main(process, links_file, humans_file, git_path):
    repo = dulwich.repo.Repo(git_path)

    if process:
        with open(links_file, 'a') as l:
            with open(humans_file, 'r') as h:
                process_humans(l, h, repo)
    else:
        with open(links_file, 'w') as l:
            links = csv.writer(l)
            with open(humans_file, 'w') as h:
                humans = csv.writer(h)
                for each in get_links(repo):
                    if len(each.bug_ids) > 1:
                        humans.writerow((each.commit_id,) + each.bug_ids)
                    elif len(each.bug_ids) == 1:
                        links.writerow([each.commit_id, each.bug_ids[0]])
