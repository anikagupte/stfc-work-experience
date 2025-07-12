#!/usr/bin/python3
"""
This script calculates the average time from creation
to merge of all merged pull requests in a repository.

"""
import github
import time
from github import Github, Auth
from prometheus_client import start_http_server, Gauge

average_seconds = Gauge('average_seconds', 'Average time to merge')

def merge_date(pr: github.Github):
    """
    find date that pull request was merged at
    :param pr: pull request object
    """
    merged = pr.merged_at
    return merged

def create_date(pr: github.Github):
    """
    find date that pull request was created at
    :param pr: pull request object
    """
    created = pr.created_at
    return created

def average_time(prs):
    """
    calculate average time that pull requests
    were merged by (in seconds)
    :param prs: list of pull request objects
    """
    for pull_request in prs:
        if pull_request.merged:
            md = merge_date(pull_request)
            cd = create_date(pull_request)
            diff.append((md - cd).total_seconds())

            print(pull_request.number)

    total = 0
    for num in diff:
        total += num
    total /= len(diff)

    return total

if __name__ == '__main__':

    start_http_server(8000)

    auth = Auth.Token("PERSONAL_ACCESS_TOKEN")
    g = Github(auth=auth)
    repo = g.get_repo("stfc/cloud-helm-charts")
    prs = repo.get_pulls(state="all")
    diff = []

    while True:
        time_sec = average_time(prs)
        average_seconds.set(time_sec)
        print(f'the average time from creation to merge is {time_sec} seconds')
        time.sleep(120)

        g.close()
