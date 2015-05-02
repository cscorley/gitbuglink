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
trigger_words = "issue|problem|bug|fix|fixing|fixes|close|closes|pr|br|bz|bugzilla"
bugids = re.compile("(?:" + trigger_words + ")\\s*(?:id|[#=])?\\s*([0-9]+)",
        flags=re.IGNORECASE)
plurals = re.compile("(?:" + trigger_words + ")s\\s*(?:id|[#=])?\\s*([0-9]+)",
        flags=re.IGNORECASE)
idnumbers = re.compile("(?:id|[#=])\\s*([0-9]+)", flags=re.IGNORECASE)
numbers = re.compile("([0-9]+)", flags=re.IGNORECASE)
bugzillaURLs = re.compile("(?:http|https)://\S+/show_bug.cgi\?id=([0-9]+)")

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


def process_files(links, humans, repo):
    # for each in humans_file,
    #   display commit
    #   display list of detected ids
    #   input corrected list
    #   append result to links_file

    for row in humans:
        commit = repo[row[0]]
        items = row[1:]
        confirmed_ids = list()

        print()
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
            links.writerow([commit.id] + confirmed_ids)


@click.command()
@click.option('--process', is_flag=True,
              help="Manually process the humans file")
@click.option('--verify', is_flag=True,
              help="Manually verify the links file")
@click.option('--links_file', default='links.csv',
              help='Output file for links')
@click.option('--humans_file', default='humans.csv',
              help='Output file for links humans need to check')
@click.option('--verified_file', default='verified.csv',
              help='Output file for links that have been manually verified')
@click.argument('git_path', type=click.Path(exists=True))
def main(process, verify, verified_file, links_file, humans_file, git_path):
    repo = dulwich.repo.Repo(git_path)

    if process:
        with open(links_file, 'a') as l:
            links = csv.writer(l)
            with open(humans_file, 'r') as h:
                humans = csv.reader(h)
                process_files(links, humans, repo)
    elif verify:
        with open(verified_file, 'a') as v:
            verified = csv.writer(v)
            with open(links_file, 'r') as l:
                links = csv.reader(l)
                process_files(verified, links, repo)
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
