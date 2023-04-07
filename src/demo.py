#!/usr/bin/env python3
""" Automatically prioritize/rank JIRA stories attached to a JIRA feature

Problem: If features are prioritized/ranked up or down - that action doesn't cascade to
stories.  In order to plan sprints, you manually have to open tons of tabs, compare the
priority/ranking of Features, find all the epics on those features and then find all the
stories for your team on those epics - and move them up in your sprint planning backlog
individually. What a pain!

This script attempts to automate that for you.

This script accepts two arguments: a project id and a token.  All of the stories of
all of the epics of the project will be checked against their parent to calculate the
right priority/rank.

Issues that do not have a parent will be labelled as 'Non-compliant'.
"""

import os

import jira

from utils.jira import update

jira_client = jira.client.JIRA(
    server="https://issues.redhat.com",
    token_auth="NzI2ODc4MzUyODczOvpPgbUZPsfJ7DUZ5JmTbqxo6qCs",
)


def main() -> None:
    setup_features()
    setup_epics()
    setup_stories()


def setup_features() -> None:
    issues = ["SPTEST-172", "SPTEST-174", "SPTEST-173"]
    priorities = ["Major", "Normal", "Normal"]
    set_priorities(issues, priorities)
    rank_issues(issues)


def setup_epics() -> None:
    issues = [
        "SPTEST-175",
        "SPTEST-176",
        "SPTEST-181",
        "SPTEST-177",
        "SPTEST-180",
        "SPTEST-178",
        "SPTEST-179",
    ]
    priorities = ["Minor", "Major", "Normal", "Undefined", "Normal", "Normal", "Normal"]
    set_priorities(issues, priorities)
    rank_issues(issues)


def setup_stories() -> None:
    issues = [
        "SPTEST-193",
        "SPTEST-191",
        "SPTEST-187",
        "SPTEST-192",
        "SPTEST-188",
        "SPTEST-189",
        "SPTEST-186",
        "SPTEST-185",
        "SPTEST-194",
        "SPTEST-190",
        "SPTEST-182",
        "SPTEST-183",
        "SPTEST-195",
        "SPTEST-184",
    ]
    priorities = [
        "Minor",
        "Major",
        "Normal",
        "Undefined",
        "Normal",
        "Normal",
        "Normal",
        "Minor",
        "Undefined",
        "Undefined",
        "Normal",
        "Undefined",
        "Normal",
        "Undefined",
    ]
    set_priorities(issues, priorities)
    rank_issues(issues)


def set_priorities(issues: list, priorities: list):
    for issue_key, priority in zip(issues, priorities):
        issue = jira_client.issue(issue_key)

        if issue.fields.priority.name != priority:
            print("Setting priority for", issue_key)
            update(issue, {"priority": {"name": priority}})

        try:
            issue.fields.labels.remove("Non-compliant")
            print("Cleaning label for", issue_key)
            update(issue, {"fields": {"labels": issue.fields.labels}})
        except ValueError:
            pass

        comments = jira_client.comments(issue_key)
        if comments:
            print("Cleaning comments for", issue_key)
            for comment in comments:
                comment.delete()


def rank_issues(issues: list):
    prev_issue = None
    for issue in issues:
        print("Setting rank for", issue)
        if prev_issue:
            jira_client.rank(issue, prev_issue=prev_issue)
        prev_issue = issue


if __name__ == "__main__":
    main()
